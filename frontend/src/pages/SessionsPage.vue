<template>
    <div class="text-h4 text-weight-bold q-ma-xs">
        Сеансы
    </div>
    <div v-if="loading" class="text-center q-pa-lg">
        <q-spinner size="50px" color="primary" />
    </div>

    <div v-else>
        <div v-if="sessions.length === 0" class="text-center q-pa-lg">
            Нет доступных сеансов
        </div>

        <q-list v-else bordered separator>
            <q-item v-for="session in sessions" :key="session.id" class="q-mb-sm">
                <q-item-section>
                    <q-item-label class="text-h6">{{ session.date }} в {{ session.time }}</q-item-label>
                    <q-item-label caption>
                        Зал: {{ session.hall.name }} |
                        Рядов: {{ session.hall_rows }} |
                        Мест в ряду: {{ session.hall_seats }}
                    </q-item-label>
                </q-item-section>

                <q-item-section side>
                    <q-btn color="grey-9" label="Выбрать места"
                        @click="$router.push(`/sessions/${session.id}/seats`)" />
                </q-item-section>
            </q-item>
        </q-list>
    </div>




</template>
<script setup>
import axios from "axios"
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const loading = ref(false)
const sessions = ref([])
const showId = computed(() => route.params.id)

const loadSessions = async () => {
    loading.value = true

    try {
        const response = await axios.get(`/api/shows/${showId.value}/sessions`)
        console.log('Полный ответ API:', response)
        console.log('Данные:', response.data)
        sessions.value = response.data
    } catch (error) {
        console.log(error)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    loadSessions()
})

</script>