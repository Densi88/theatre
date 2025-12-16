<template>
    <q-page class="q-pa-lg">
        <!-- Кнопка назад -->
        <q-btn flat icon="arrow_back" label="Назад" class="q-mb-lg" @click="$router.back()" />

        <div v-if="loading" class="text-center text-grey-6">
            Загрузка новости...
        </div>

        <div v-else class="row items-start q-col-gutter-md">

            <!-- Текст новости -->
            <div class="col-12 col-md-6">
                <div class="text-h4 text-weight-bold q-mb-md">{{ news.title }}</div>
                <div class="text-caption text-grey-6 q-mb-md">{{ formatDate(news.published_at) }}</div>
                <div class="text-body1" style="white-space: pre-line;">
                    {{ news.description }}
                </div>
            </div>

            <!-- Картинка новости -->
            <div class="col-12 col-md-6">
                <q-img :src="getImageUrl(news.news_image)" :ratio="16 / 9" class="rounded-borders shadow-2"
                    spinner-color="primary" :fallback-src="'https://via.placeholder.com/800x450?text=No+Image'" />
            </div>

        </div>
    </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from "axios"
import { date } from 'quasar'

const route = useRoute()
const news = ref({})
const loading = ref(true)

const loadNews = async () => {
    loading.value = true
    const id = route.params.id
    try {
        const response = await axios.get(`/api/news/${id}/`)
        news.value = response.data
        console.log("ОТВЕТ ОТ АПИ", response.data)
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
}

const getImageUrl = (imagePath) => {
    if(!imagePath){
    return 
  }
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        console.log('URL уже полный:', imagePath)
        return imagePath
    }

    return imagePath
}

const formatDate = (isoString) => {
    if (!isoString) return ''
    return date.formatDate(isoString, 'DD MMMM YYYY, HH:mm')
}



onMounted(loadNews)
</script>

<style scoped>
.rounded-borders {
    border-radius: 12px;
}

.shadow-2 {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>
