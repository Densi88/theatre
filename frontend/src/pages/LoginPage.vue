<template>
    <q-page class="flex flex-center">
        <q-card style="width: 350px">
            <q-card-section>
                <div class="text-h6">Вход</div>
            </q-card-section>

            <q-card-section>
                <q-form @submit.prevent="handleLogin" class="q-gutter-md">
                    <q-input v-model="form.username" label="Логин" outlined :rules="[val => !!val || 'Обязательно']" />

                    <q-input v-model="form.password" label="Пароль" type="password" outlined
                        :rules="[val => !!val || 'Обязательно']" />

                    <q-btn type="submit" label="Войти" color="primary" class="full-width" :loading="loading" />

                    <div class="text-center">
                        <q-btn flat label="Регистрация" @click="$router.push('/register')" />
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'stores/auth'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const loading = ref(false)
const form = ref({
    username: '',
    password: ''
})

const handleLogin = async () => {
    loading.value = true

    const result = await authStore.login(form.value.username, form.value.password)

    if (result.success) {
        $q.notify({ type: 'positive', message: 'Вход выполнен' })
        router.push('/')
    } else {
        $q.notify({ type: 'negative', message: result.message || 'Ошибка входа' })
    }

    loading.value = false
}
</script>