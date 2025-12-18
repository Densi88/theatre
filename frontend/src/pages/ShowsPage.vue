<template>
    <!-- Поиск -->
    <div class="row q-mb-md">
        <q-input v-model="searchQuery" placeholder="Поиск спектаклей..." outlined clearable
            @update:model-value="loadShows" class="col-12 col-md-6">
            <template v-slot:append>
                <q-icon name="search" />
            </template>
        </q-input>
         <q-select v-model="selectedGenre" :options="genres" label="Жанр" outlined clearable
            @update:model-value="loadShows" class="col-12 col-md-3" option-label="genre_name" option-value="id"/>
    </div>
       
    <div class="text-h4 text-weight-bold q-ma-xs">
        Спектакли
    </div>

    <div class="q-ma-xs">
        <q-btn v-if="authStore.is_staff" color="grey-9" icon="add" label="Добавить" @click="openAddDialog()" />
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
                <q-card-actions align="left">
                    <div class="q-ma-xs">
                        <q-btn v-if="authStore.is_staff" color="grey-9" icon="delete" label="Удалить" @click.stop="deleteShow(showItem)" />
                    </div>
                    <div class="q-ma-xs">
                        <q-btn v-if="authStore.is_staff" color="grey-9" icon="update" label="Изменить" @click.stop="openUpdateDialog(showItem)" />
                    </div>
                </q-card-actions>
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

    <q-dialog v-model="updateDialog">
        <q-card style="min-width: 400px;">
            <q-card-section>
                <div class="text-h6">Редактировать спектакль</div>
            </q-card-section>

            <q-card-section>
                <q-input v-model="updatedShow.title" label="Название" outlined />
                <q-input v-model="updatedShow.description" label="Описание" type="textarea" outlined class="q-mt-sm" />
                <!-- Загрузка файла постера -->
                <q-file v-model="updatedShow.poster" label="Постер спектакля" outlined accept="image/*"
                    class="q-mt-sm" />
                <q-select v-model="updatedShow.actor" :options="actors" label="Актеры" multiple emit-value
                    option-value="value" option-label="label" use-input outlined class="q-mt-sm" />

                <q-select v-model="updatedShow.genre" :options="genres" label="Жанры" multiple emit-value
                    option-value="value" option-label="label" use-input class="q-mt-sm" />
                <q-input v-model="updatedShow.duration" label="Длительность" outlined class="q-mt-sm" />
            </q-card-section>

            <q-card-actions align="right">
                <q-btn flat label="Отмена" color="negative" v-close-popup />
                <q-btn flat label="Добавить" color="primary" @click="updateShow" />
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
const totalCount = ref(0)
const router = useRouter()
const actors = ref([])
const genres = ref([])
const searchQuery = ref('')
const selectedGenre = ref(null)
import { UseAuthStore } from 'stores/auth'
const authStore=UseAuthStore()
const addDialog = ref(false)
const updateDialog = ref(false)
const newShow = ref({
    title: '',
    description: '',
    poster: null,
    actor: [],
    genre: [],
    duration: ''
})
const updatedShow = ref({
    id: '',
    title: '',
    description: '',
    poster: null,
    actor: [],
    genre: [],
    duration: ''
})

const loadShows = async () => {
    loading.value = true
    const params={}
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    if (selectedGenre.value) {
      params.genre = selectedGenre.value.id
    }

    try {
        const response = await axios.get('/api/shows/', {params})
        console.log('Полный ответ API:', response) 
        console.log('Данные:', response.data) 
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
    if(!imagePath){
    return 
  }
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
    router.push(`/shows/${showItem.id}/sessions`)
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
        actors.value = actorsResp.data.map(a => ({
            label: a.name,
            value: String(a.id)
        }))
        console.log('Actors loaded:', actors.value)

        const genresResp = await axios.get('/api/genres')
        genres.value = genresResp.data.map(g => ({
            label: g.genre_name,
            value: String(g.id)
        }))
        console.log('Genres loaded:', genres.value)

    } catch (error) {
        console.error('Ошибка загрузки:', error)
    }
    console.log('actors array:', actors.value)
    console.log('first actor:', actors.value[0])
}
const deleteShow = async (showItem) => {
    try {
        const confirmDelete = window.confirm(`Удалить спектакль "${showItem.title}"?`)
        if (!confirmDelete) return
        await axios.delete(`/api/shows/${showItem.id}/`)

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
const openUpdateDialog = (showItem) => {
    console.log(showItem.actor)
    console.log(showItem.genre)
    const actorIds = showItem.actor.map(a => {
        const id = typeof a === 'object' ? a.id : a
        return String(id)  // ← В строку!
    })

    const genreIds = showItem.genre.map(g => {
        const id = typeof g === 'object' ? g.id : g
        return String(id)
    })

    updatedShow.value = {
        id: showItem.id, title: showItem.title, description: showItem.description, poster: showItem.poster, actor: actorIds,
        genre: genreIds, duration: showItem.duration
    }
    updateDialog.value = true

}
const updateShow = async () => {
    try {
        const formData = new FormData()
        formData.append('title', updatedShow.value.title)
        formData.append('description', updatedShow.value.description)
        formData.append('duration', String(updatedShow.value.duration))
        updatedShow.value.actor.forEach(id => {
            const cleanId = String(id).replace(/^,/, '').trim()
            if (cleanId) formData.append('actor', cleanId)
        })

        updatedShow.value.genre.forEach(id => {
            const cleanId = String(id).replace(/^,/, '').trim()
            if (cleanId) formData.append('genre', cleanId)
        })

        // КЛЮЧЕВОЕ: проверяем, это файл или URL
        if (updatedShow.value.poster instanceof File) {
            formData.append('poster', updatedShow.value.poster)
            console.log('Adding new poster file:', updatedShow.value.poster.name)
        } else if (updatedShow.value.poster) {
            console.log('Keeping old poster:', updatedShow.value.poster)
        }

        console.log('FormData contents:')
        for (let [key, value] of formData.entries()) {
            console.log(key, ':', value, 'type:', typeof value)
        }

        const response = await axios.patch(
            `/api/shows/${updatedShow.value.id}/`,
            formData
        )

        console.log('Success!', response.data)
        $q.notify({ type: 'positive', message: 'Спектакль обновлён!' })
        await loadShows()
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
    loadShows()
    loadActorsAndGenres()
})

</script>
