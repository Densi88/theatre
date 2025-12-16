<template>
    <q-page class="q-pa-lg">
        <!-- Кнопка назад -->
        <q-btn flat icon="arrow_back" label="Назад" class="q-mb-lg" @click="$router.back()" />

        <div v-if="loading" class="text-center text-grey-6">
            Загрузка профиля
        </div>

        <div v-else class="row items-start q-col-gutter-md">
            <div class="col-12 col-md-6">
                <div class="text-h3 text-weight-bold q-ma-md">{{full_name}}</div>
                <div class="text-h4 text-weight-bold q-ma-md">Ваш email: {{email}}</div>
                <div class="text-h4 text-weight-bold q-ma-md">Имя пользователя: {{username}}</div>
            </div>
            <div class="col-12 col-md-6">
                <q-img src="/user_log.png" ratio="16 / 9" class="rounded-borders shadow-2"
                    spinner-color="primary" :fallback-src="'https://via.placeholder.com/800x450?text=No+Image'" />
            </div>

        </div>
    </q-page>
</template>

<script setup>
import { UseAuthStore } from 'stores/auth'
import { onBeforeMount, ref } from 'vue';
const authStore = UseAuthStore()
const loading = ref(true)
const email=ref()
const full_name=ref()
const username=ref()
const setUserInfo=()=>{
    email.value=authStore.email
    full_name.value=authStore.full_name
    username.value=authStore.username
    loading.value=false
}

onBeforeMount(() => {
   authStore.fetchUserInfo()
    setUserInfo()
})
</script>