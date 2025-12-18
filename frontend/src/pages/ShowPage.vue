<template>
    <q-page class="q-pa-lg">
        <!-- Кнопка назад -->
        <q-btn flat icon="arrow_back" label="Назад" class="q-mb-lg" @click="$router.back()" />

        <div v-if="loading" class="text-center text-grey-6">
            Загрузка спектакля...
        </div>

        <div v-else class="row items-start q-col-gutter-md">

            <div class="col-12 col-md-6">
                <div class="text-h4 text-weight-bold q-mb-md">{{ show.title }}</div>
                <div class="text-body1" style="white-space: pre-line;">
                    {{ show.description }}
                </div>
                <div class="text-body1 text-weight-bold" style="white-space: pre-line;">
                    Жанр: {{ show.genre.map(g => g.genre_name).join(', ') }}
                </div>
                <div class="text-body1 text-weight-bold" style="white-space: pre-line;">
                    Актеры: {{ show.actor.map(a => a.name).join(', ') }}
                </div>
                <div class="text-body1 text-weight-bold" style="white-space: pre-line;">
                    Длительность(мин): {{show.duration }}
                </div>
            </div>

            <!-- Картинка новости -->
            <div class="col-12 col-md-6">
                <q-img :src="computed(() => show?.poster || '')" :ratio="16 / 9" class="rounded-borders shadow-2"
                    spinner-color="primary" :fallback-src="'https://via.placeholder.com/800x450?text=No+Image'" />
            </div>

        </div>
    </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from "axios"
const route = useRoute()
const show = ref({})
const loading = ref(true)

const load = async () => {
    loading.value = true
    const id = route.params.id
    try {
        const response = await axios.get(`/api/shows/${id}/`)
        show.value = response.data
        console.log("ОТВЕТ ОТ АПИ", response.data)
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
}
onMounted(load)
</script>

<style scoped>
.rounded-borders {
    border-radius: 12px;
}

.shadow-2 {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>
