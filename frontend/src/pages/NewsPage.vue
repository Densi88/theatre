<template>
  <div class="text-h4 text-weight-bold q-mb-md">
    Новости нашего театра
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
                {{ formatDate(newsItem.published_at) }}
              </div>
            </div>
            
            <!-- Лейбл "Новое" для свежих новостей -->
            <div 
              v-if="isNewNews(newsItem.published_at)"
              class="absolute-top-left bg-positive text-white q-pa-xs q-ma-sm rounded-borders"
            >
              <q-icon name="fiber_new" size="sm" />
              <span class="text-caption q-ml-xs">Новое</span>
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
        </q-card>
      </div>
    </div>
    

    
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import axios from "axios"


const $q = useQuasar()
// Состояние
const news = ref([])
const loading = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(9)
const totalCount = ref(0)
const sortOrder = ref('-published_at')

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

    console.log('Ответ от API:', response.data) // Добавьте это
    console.log('Тип данных:', typeof response.data) // Добавьте это
    
    // Проверяем структуру ответа
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

const getImageUrl = (imagePath) => {
  console.log('📸 Получение URL изображения:', imagePath)
  // Если путь уже полный URL, возвращаем как есть
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    console.log('📸 URL уже полный:', imagePath)
    return imagePath
  }
  
  // Для относительных путей
  console.log('📸 Относительный путь, добавляем базовый URL')
  return imagePath
}

const truncateText = (text, maxLength = 150) => {
  console.log('✂️ Обрезка текста:', text?.substring(0, 50) + '...')
  
  if (!text || typeof text !== 'string') {
    console.log('✂️ Текст отсутствует или не строка')
    return 'Описание отсутствует'
  }
  
  const trimmed = text.trim()
  
  if (trimmed.length <= maxLength) {
    console.log('✂️ Текст не требует обрезки')
    return trimmed
  }
  
  const result = trimmed.substring(0, maxLength) + '...'
  console.log('✂️ Обрезано до:', result)
  return result
}

const getFirstTwoSentences = (text) => {
  console.log('📝 Получение первых двух предложений')
  
  if (!text || typeof text !== 'string') {
    console.log('📝 Текст отсутствует')
    return ''
  }
  
  const trimmed = text.trim()
  
  // Простая логика для русских предложений
  const sentences = trimmed.match(/[^.!?]+[.!?]+/g) || [trimmed]
  
  console.log('📝 Найдено предложений:', sentences.length)
  
  if (sentences.length === 0) return ''
  
  // Берем первые два предложения
  const firstTwo = sentences.slice(0, 2).join(' ')
  
  // Обрезаем если слишком длинные
  const result = truncateText(firstTwo, 200)
  console.log('📝 Результат:', result)
  return result
}

onMounted(() => {
  loadNews()
})
</script>
