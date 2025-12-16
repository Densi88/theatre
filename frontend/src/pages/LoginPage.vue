<template>
    
    <q-page class="flex flex-center">
        <q-card style="width: 350px">
            <q-card-section>
                <div class="text-h6">Вход</div>
            </q-card-section>

            <q-card-section>
                <q-form class="q-gutter-md">
                    <q-input 
                        v-model="formData.username" 
                        label="Логин" 
                        outlined 
                        :rules="[val => !!val || 'Обязательно']" 
                    />

                    <q-input 
                        v-model="formData.password" 
                        label="Пароль" 
                        type="password" 
                        outlined
                        :rules="[val => !!val || 'Обязательно']" 
                    />

                    <q-btn
                        @click="submitLogin()" 
                        type="submit" 
                        label="Войти" 
                        color="primary" 
                        class="full-width" 
                    />

                    <div class="text-center">
                        <q-btn flat label="Регистрация" @click="$router.push('/register')" />
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </q-page>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { UseAuthStore } from 'src/stores/auth';
import { useRouter } from 'vue-router'
const router = useRouter()


const formData = ref({
    username: '',
    password: ''
});
const authStore = UseAuthStore()

const submitLogin = async () => {
    try {
        console.log('Пытаюсь войти с:', formData.value.username);
        
        const r = await axios.post("/api/users/login/", {
            username: formData.value.username,
            password: formData.value.password
        });
        
        console.log(r.data);
        authStore.updateCsrfToken()
         router.push('/')
        
        
    } catch (error) {
        console.error('Ошибка входа:', error);
        console.error('Ответ сервера:', error.response?.data);
    }
};
</script>