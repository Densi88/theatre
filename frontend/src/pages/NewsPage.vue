<template>
  <div class="text-h4 text-weight-bold q-mb-md">
    Новости нашего театра
  </div>
  <div class="q-mb-md">
        <q-btn color="primary" icon="add" label="Добавить" @click="openAddDialog()" />
    </div>


   <div v-if="loading" class="row q-col-gutter-md">
      <div v-for="n in 3" :key="n" class="col-12 col-md-4">
        <q-card class="news-card">
          <q-skeleton height="200px" square />
          <q-card-section>
            <q-skeleton type="text" class="text-subtitle1" />
            <q-skeleton type="text" width="80%" />
            <q-skeleton type="text" width="60%" />
          </q-card-section>
        </q-card>
      </div>
    </div>

    <div v-else class="row q-col-gutter-lg">
      <div 
        v-for="newsItem in news" 
        :key="newsItem.id"
        class="col-12 col-md-6 col-lg-4"
      >
        <q-card 
          class="news-card cursor-pointer hover-card"
          @click="viewNewsDetail(newsItem)"
        >
          <!-- Картинка новости -->
          <q-img
            :src="getImageUrl(newsItem.news_image)"
            :ratio="16/9"
            class="news-image"
          >
            <!-- Дата публикации поверх картинки -->
            <div class="absolute-top-right bg-primary text-white q-pa-xs q-ma-sm rounded-borders">
              <div class="text-caption text-weight-bold">
                {{formattedDate(newsItem.published_at)}}
              </div>
            </div>
          </q-img>
          
          <q-card-section>
            <!-- Краткое описание -->
            <div class="news-preview">
              <div class="text-body1 text-weight-medium q-mb-sm">
                {{ truncateText(newsItem.description, 150) }}
              </div>
              
              <!-- Первые два предложения -->
              <div class="text-body2 text-grey-7">
                {{ getFirstTwoSentences(newsItem.description) }}
              </div>
            </div>
          </q-card-section>
          
          <q-card-actions align="right">
            <q-btn
              flat
              color="primary"
              icon="arrow_forward"
              label="Читать далее"
              @click.stop="viewNewsDetail(newsItem)"
            />
          </q-card-actions>
          <q-card-actions align="left">
                    <div class="q-mb-md">
                        <q-btn color="primary" icon="add" label="Удалить" @click.stop="deleteNew(newsItem)" />
                    </div>
                    <div class="q-mb-md">
                        <q-btn color="primary" icon="add" label="Изменить" @click.stop="openUpdateDialog(newsItem)" />
                    </div>
                </q-card-actions>
        </q-card>
      </div>
    </div>

    <q-dialog v-model="addDialog">
        <q-card style="min-width: 400px;">
            <q-card-section>
                <div class="text-h6">Добавить новую новость</div>
            </q-card-section>

            <q-card-section>
                <q-input v-model="newNews.description" label="Текст" type="textarea" outlined class="q-mt-sm" />
                <q-file v-model="newNews.news_image" label="Картинка" outlined accept="image/*" class="q-mt-sm" />
            </q-card-section>

            <q-card-actions align="right">
                <q-btn flat label="Отмена" color="negative" v-close-popup />
                <q-btn flat label="Добавить" color="primary" @click="submitAdd()" />
            </q-card-actions>
        </q-card>
    </q-dialog>

    <q-dialog v-model="updateDialog">
        <q-card style="min-width: 400px;">
            <q-card-section>
                <div class="text-h6">Редактировать новость</div>
            </q-card-section>

            <q-card-section>
                <q-input v-model="updateNews.description" label="Текст" type="textarea" outlined class="q-mt-sm" />
                <q-file v-model="updateNews.news_image" label="Картинка" outlined accept="image/*" class="q-mt-sm" />
            </q-card-section>

            <q-card-actions align="right">
                <q-btn flat label="Отмена" color="negative" v-close-popup />
                <q-btn flat label="Редактировать" color="primary" @click="submitUpdate()" />
            </q-card-actions>
        </q-card>
    </q-dialog>
    
    

    
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import axios from "axios"
import { useRouter } from 'vue-router'
import { computed } from 'vue'


const $q = useQuasar()
const news = ref([])
const loading = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(9)
const totalCount = ref(0)
const sortOrder = ref('-published_at')
const addDialog=ref(false)
const updateDialog=ref(false)
const newNews = ref({
    description: '',
    news_image: null,
    published_at: ''
})
const updateNews=ref({
  id: '',
  description: '',
  news_image: null,
})


const router = useRouter()

const loadNews = async () => {
  loading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      page_size: itemsPerPage.value,
      ordering: sortOrder.value
    }
    
    const response = await axios.get('/api/news/', { params })
    news.value = response.data.results || response.data
    totalCount.value = response.data.count || response.data.length
    
    if (response.data.results) {
      news.value = response.data.results
      totalCount.value = response.data.count || 0
    } else if (Array.isArray(response.data)) {
      news.value = response.data
      totalCount.value = response.data.length
    } else {
      console.error('Неожиданная структура ответа:', response.data)
    }

    
    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при загрузке новостей',
      caption: error.message
    })
  } finally {
    loading.value = false
  }
}

const formattedDate = computed(() => {
  return (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
})

const getImageUrl = (imagePath) => {
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    console.log('URL уже полный:', imagePath)
    return imagePath
  }
  
  return imagePath
}

const truncateText = (text, maxLength = 150) => {
  
  if (!text || typeof text !== 'string') {
    return 'Описание отсутствует'
  }
  
  const trimmed = text.trim()
  
  if (trimmed.length <= maxLength) {
    return trimmed
  }
  
  const result = trimmed.substring(0, maxLength) + '...'
  return result
}

const getFirstTwoSentences = (text) => {
  if (!text || typeof text !== 'string') {
    return ''
  }
  
  const trimmed = text.trim()
  
  const sentences = trimmed.match(/[^.!?]+[.!?]+/g) || [trimmed]
  
  if (sentences.length === 0) return ''
  
  const firstTwo = sentences.slice(0, 2).join(' ')
  
  const result = truncateText(firstTwo, 200)
  return result
}

const viewNewsDetail=(newsItem)=>{
  router.push(`/news/${newsItem.id}`)  
}
const openAddDialog=()=>{
  const currentTime = new Date().toISOString()
  newNews.value={title: '', description:'', published_at: currentTime}
  addDialog.value=true
}
const  submitAdd=async()=>{
   if (!newNews.value.description) {
        $q.notify({ type: 'warning', message: 'Заполните все поля' })
        return
    }

    try {
        const formData = new FormData()
        formData.append('description', newNews.value.description)

        if (newNews.value.news_image) {
            formData.append('news_image', newNews.value.news_image)
        }

        const response = await axios.post('/api/news/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })

        $q.notify({ type: 'positive', message: 'Новость добавлена' })
        news.value.push(response.data)
        addDialog.value = false
    } catch (error) {
        console.error(error)
        $q.notify({
            type: 'negative',
            message: 'Ошибка при добавлении',
            caption: error.response?.data || error.message
        })
    }
}
const openUpdateDialog=(newsItem)=>{
  updateNews.value={id:newsItem.id, description:newsItem.description, news_image: newsItem.news_image}
  updateDialog.value=true

}
const submitUpdate=async()=>{
  try {
        const formData = new FormData()
        formData.append('description', updateNews.value.description)
        if (updateNews.value.news_image instanceof File) {
            formData.append('news_image', updateNews.value.news_image)
        } else if (updateNews.value.news_image) {
            console.log('Keeping old poster:', updateNews.value.news_image)
        }
        console.log('FormData contents:')
        for (let [key, value] of formData.entries()) {
            console.log(key, ':', value, 'type:', typeof value)
        }
        
        const response = await axios.patch(
            `/api/news/${updateNews.value.id}/`,
            formData  
        )
        
        console.log('Success!', response.data)
        $q.notify({ type: 'positive', message: 'Новость обновлена!' })
        await loadNews()
        updateDialog.value = false
        
    } catch (error) {
        console.error('Full error:', error)
        console.error('Response data:', error.response?.data)
        $q.notify({
            type: 'negative',
            message: 'Ошибка обновления',
            caption: error.response?.data ? JSON.stringify(error.response.data) : error.message
        })
    }

}

onMounted(() => {
  loadNews()
})
</script>
