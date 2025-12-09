<template>
  <q-card class="news-detail-card">
    <q-card-section class="q-pa-none">
      <!-- Кнопка закрытия -->
      <div class="row justify-end q-pa-sm">
        <q-btn
          icon="close"
          round
          dense
          flat
          @click="$emit('close')"
        />
      </div>
      
      <!-- Картинка -->
      <q-img
        :src="getImageUrl(newsItem.news_image)"
        :ratio="21/9"
        class="detail-image"
      >
        <div class="absolute-bottom bg-dark-transparent text-white q-pa-lg">
          <div class="text-h5 text-weight-bold">
            {{ formatDate(newsItem.published_at) }}
          </div>
        </div>
      </q-img>
    </q-card-section>
    
    <q-card-section class="q-pt-xl">
      <!-- Полный текст -->
      <div class="news-content">
        <div class="text-h4 text-weight-bold q-mb-lg">
          Новость
        </div>
        
        <div class="text-body1 q-mb-xl line-height-2">
          {{ newsItem.description }}
        </div>
        
        <!-- Дополнительная информация -->
        <div class="row items-center q-mt-xl">
          <div class="col">
            <div class="text-caption text-grey-6">
              Опубликовано: {{ formatDateTime(newsItem.published_at) }}
            </div>
          </div>
          <div class="col-auto">
            <q-btn
              color="primary"
              icon="share"
              label="Поделиться"
              @click="shareNews"
            />
          </div>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { useQuasar } from 'quasar'
import api from '../services/api'

const props = defineProps({
  newsItem: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

const $q = useQuasar()

// Вспомогательные функции
const getImageUrl = (imagePath) => {
  if (!imagePath) return '/placeholder-news.jpg'
  
  if (imagePath.startsWith('http')) {
    return imagePath
  }
  return `${api.defaults.baseURL}${imagePath}`
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const shareNews = () => {
  if (navigator.share) {
    navigator.share({
      title: 'Новость театра',
      text: props.newsItem.description.substring(0, 100) + '...',
      url: window.location.href,
    })
  } else {
    $q.notify({
      message: 'Ссылка скопирована в буфер обмена',
      color: 'positive',
      icon: 'content_copy'
    })
    
    // Копирование URL в буфер обмена
    navigator.clipboard.writeText(window.location.href)
  }
}
</script>

<style scoped>
.news-detail-card {
  max-width: 900px;
  margin: 0 auto;
}

.detail-image {
  max-height: 400px;
}

.bg-dark-transparent {
  background-color: rgba(0, 0, 0, 0.6);
}

.news-content {
  max-width: 800px;
  margin: 0 auto;
}

.line-height-2 {
  line-height: 2;
}

@media (max-width: 600px) {
  .news-detail-card {
    margin: 0;
    border-radius: 0;
  }
  
  .detail-image {
    max-height: 250px;
  }
}
</style>