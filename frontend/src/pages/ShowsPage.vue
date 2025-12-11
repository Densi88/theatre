<template>
    <div class="text-h4 text-weight-bold q-mb-md">
        Спектакли
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
        <div v-for="showItem in shows" :key="showItem.id" class="col-12 col-md-6 col-lg-4">
            <q-card class="news-card cursor-pointer hover-card" @click="viewShowDetail(showItem)">
                <q-img :src="getImageUrl(showItem.poster)" :ratio="16 / 9" class="show-image">
                </q-img>

                <q-card-section>
                    <!-- Краткое описание -->
                    <div class="news-preview">
                        <div class="text-body1 text-weight-bold q-mb-sm">
                            {{ showItem.title }}
                        </div>
                    </div>
                </q-card-section>

                <q-card-section>
                    <!-- Краткое описание -->
                    <div class="news-preview">
                        <div class="text-body1 text-weight-medium q-mb-sm">
                            {{ truncateText(showItem.description, 150) }}
                        </div>
                    </div>
                </q-card-section>

                <q-card-actions align="right">
                    <q-btn flat color="primary" icon="arrow_forward" label="Читать далее"
                        @click.stop="viewShowDetail(showItem)" />
                </q-card-actions>
                <q-card-actions align="right">
                    <q-btn flat color="primary" icon="arrow_forward" label="Купить" @click.stop="buyShow(showItem)" />
                </q-card-actions>
                <div class="q-mb-md">
                    <q-btn color="primary" icon="add" label="Удалить" @click.stop="deleteShow(showItem)" />
                </div>
            </q-card>
        </div>
    </div>

    <q-dialog v-model="addDialog">
        <q-card style="min-width: 400px;">
            <q-card-section>
                <div class="text-h6">Добавить новый спектакль</div>
            </q-card-section>

            <q-card-section>
                <q-input v-model="newShow.title" label="Название" outlined />
                <q-input v-model="newShow.description" label="Описание" type="textarea" outlined class="q-mt-sm" />
                <!-- Загрузка файла постера -->
                <q-file v-model="newShow.poster" label="Постер спектакля" outlined accept="image/*" class="q-mt-sm" />
                <q-select v-model="newShow.actor" :options="actors" label="Актеры" multiple emit-value map-options
                    outlined class="q-mt-sm" />

                <q-select v-model="newShow.genre" :options="genres" label="Жанры" multiple emit-value map-options
                    outlined class="q-mt-sm" />
                <q-input v-model="newShow.duration" label="Длительность" outlined class="q-mt-sm" />
            </q-card-section>

            <q-card-actions align="right">
                <q-btn flat label="Отмена" color="negative" v-close-popup />
                <q-btn flat label="Добавить" color="primary" @click="submitAddShow" />
            </q-card-actions>
        </q-card>
    </q-dialog>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import axios from "axios"
import { useRouter } from 'vue-router'
const $q = useQuasar()
const shows = ref([])
const loading = ref(false)
// const currentPage = ref(1)
// const itemsPerPage = ref(9)
const totalCount = ref(0)
const router = useRouter()
const actors = ref([])
const genres = ref([])

const addDialog = ref(false)
const newShow = ref({
    title: '',
    description: '',
    poster: null,
    actor: [],
    genre: [],
    duration: ''
})

const loadShows = async () => {
    loading.value = true

    try {
        const response = await axios.get('/api/shows')
        console.log('Полный ответ API:', response) // Для отладки
        console.log('Данные:', response.data) // Посмотрите структуру
        shows.value = response.data
        totalCount.value = response.data.count || response.data.length
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

const viewShowDetail = (showItem) => {
    router.push(`/shows/${showItem.id}`)
}

const buyShow = (showItem) => {
    console.log('Купить билет на:', showItem)
    // Здесь будет логика покупки
}

// Открытие диалога
const openAddDialog = () => {
    newShow.value = { title: '', description: '', poster: '', genre: [], actor: [], duration: '' }
    addDialog.value = true
}

const submitAddShow = async () => {
    if (!newShow.value.title || !newShow.value.description) {
        $q.notify({ type: 'warning', message: 'Заполните все поля' })
        return
    }

    try {
        const formData = new FormData()
        formData.append('title', newShow.value.title)
        formData.append('description', newShow.value.description)
        formData.append('duration', newShow.value.duration)
        console.log('actor:', newShow.value.actor, newShow.value.actor.map(a => typeof a))
        console.log('genre:', newShow.value.genre, newShow.value.genre.map(g => typeof g))

        // Жанры и актеры
        newShow.value.actor.forEach(id => formData.append('actor', id))
        newShow.value.genre.forEach(id => formData.append('genre', id))

        console.log('poster объект:', newShow.value.poster)

        if (newShow.value.poster) {
            formData.append('poster', newShow.value.poster)
        }

        const response = await axios.post('/api/shows/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })

        $q.notify({ type: 'positive', message: 'Спектакль добавлен' })
        shows.value.push(response.data)
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
const loadActorsAndGenres = async () => {
    try {
        const actorsResp = await axios.get('/api/actors')
        actors.value = actorsResp.data.map(a => ({ label: a.name, value: a.id }))

        const genresResp = await axios.get('/api/genres')
        genres.value = genresResp.data.map(g => ({ label: g.genre_name, value: g.id }))
    } catch (error) {
        $q.notify({ type: 'negative', message: 'Ошибка при загрузке актеров или жанров', caption: error.message })
    }
}

const deleteShow=async(showItem)=>{
    try {
    const confirmDelete = window.confirm(`Удалить спектакль "${showItem.title}"?`)
    if (!confirmDelete) return
    await axios.delete(`/api/shows/${showItem.id}/`) // обратите внимание на слэш в конце!

    shows.value = shows.value.filter(s => s.id !== showItem.id)

    $q.notify({ type: 'positive', message: 'Спектакль удалён' })
  } catch (error) {
    console.error(error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при удалении',
      caption: error.response?.data || error.message
    })
  } 
}
onMounted(() => {
    loadShows()
    loadActorsAndGenres()
})

</script>
