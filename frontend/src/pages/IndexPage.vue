<template>
  <div class="text-h4 text-weight-bold q-mb-md">
    Главная
  </div>
  <div class="text-h4 text-weight-medium q-mb-md">
    Наши представления
  </div>

  <div class="row q-col-gutter-md">
    <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="showItem in shows" :key="showItem.id">
      <div class="q-card q-ma-sm"  @click="viewNewDetail(newsItem)">
        <q-img :src="getImage(showItem.poster)" :ratio="16 / 9" />

        <div class="text-body1 text-weight-bold q-mt-sm">
          {{ showItem.title }}
        </div>

        <div class="text-body1 text-weight-medium q-mb-sm">
          {{truncateText(showItem.description, 150) }}
        </div>
        <q-card-actions align="right">
          <q-btn flat color="primary" icon="arrow_forward" label="Читать далее"
            @click.stop="viewShowDetail(showItem)" />
        </q-card-actions>
        <q-card-actions align="right">
          <q-btn flat color="primary" icon="arrow_forward" label="Купить билет" @click.stop="buyShowTicket(showItem)" />
        </q-card-actions>
      </div>
    </div>
  </div>



  <div class="text-h4 text-weight-medium q-mb-md">
    <a>Наши новости</a>
  </div>

  <div class="row q-col-gutter-md">
    <div class="col-12 col-sm-6 col-md-4" v-for="newsItem in news" :key="newsItem.id">
      <div class="q-card q-ma-sm" @click="viewNewDetail(newsItem)">
        <q-img :src="getImage(newsItem.news_image)" :ratio="16 / 9" />

        <div class="text-body1 text-weight-medium q-mt-sm q-mb-sm">
          {{truncateText(newsItem.description, 150) }}
        </div>
        <q-card-actions align="right">
          <q-btn flat color="primary" icon="arrow_forward" label="Читать далее" @click.stop="viewNewsDetail(newsItem)" />
        </q-card-actions>
      </div>
    </div>
  </div>


</template>

<script setup>
import axios from "axios"
import { useRouter } from 'vue-router'
const shows = ref([])
const news = ref([])
const router = useRouter()
import { ref, onMounted } from 'vue'
const downloadFiveShows = async () => {
  const response = await axios.get('/api/shows')
  shows.value = response.data.slice(0, 5)
}
const downloadFiveNews = async () => {
  const response = await axios.get('/api/news')
  news.value = response.data.slice(0, 5) // Берем первые 5 элементов
}

const getImage = (imagePath) => {
  if(!imagePath){
    return 
  }
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    console.log('URL уже полный:', imagePath)
    return imagePath
  }

  return imagePath
}

const viewNewsDetail=(newsItem)=>{
  router.push(`/news/${newsItem.id}`)
  
}

const viewShowDetail=(showItem)=>{
  router.push(`/shows/${showItem.id}`)
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

onMounted(() => {
  downloadFiveShows()
  downloadFiveNews()
})

</script>
