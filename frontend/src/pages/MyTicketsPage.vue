<template>
    <div class="text-h4 text-weight-bold q-ma-xs">
        Мои билеты
    </div>
    <div v-if="loading" class="text-center q-pa-lg">
        <q-spinner size="50px" color="primary" />
    </div>

    <div v-else>
        <div v-if="tickets.length === 0" class="text-center q-pa-lg">
            Нет билетов
        </div>

        <q-list v-else bordered separator>
            <q-item v-for="ticket in tickets" :key="ticket.id" class="q-mb-sm">
                <q-item-section>
                    <q-item-label caption>
                        Ряд: {{ ticket.row }} |
                        Место: {{ ticket.seat }} |
                        Цена: {{ ticket.price }}
                        Сеанс:{{ ticket.session.date }}
                    </q-item-label>
                </q-item-section>
            </q-item>
        </q-list>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from "axios"
import { UseAuthStore } from 'stores/auth'
const authStore = UseAuthStore()
const loading = ref(false)
const tickets = ref([])
const userId = authStore.profile_id



const loadTickets = async () => {
    const r = await axios.get(`/api/tickets/`, {
        params: {
            user: userId  // Фильтруем по пользователю
        }
    })
    tickets.value = r.data
    console.log(r.value)
}

onMounted(() => {
    loadTickets()
    authStore.fetchUserInfo()
})
</script>