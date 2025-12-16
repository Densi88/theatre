<template>
  <q-page class="flex flex-center">
    <q-card style="width: 400px">
      <q-card-section>
        <div class="text-h6">Регистрация</div>
      </q-card-section>
      
      <q-card-section>
        <q-form @submit.prevent="handleRegister" class="q-gutter-md">
          <q-input v-model="form.username" label="Логин" outlined required />
          <q-input v-model="form.password" label="Пароль" type="password" outlined required />
          <q-input v-model="form.email" label="Email" type="email" outlined />
          <q-input v-model="form.full_name" label="ФИО" outlined required />
          <q-input v-model="form.birth_date" label="Дата рождения" type="date" outlined required />
          <q-input v-model="form.passport_series" label="Серия паспорта" type="number" outlined required />
          <q-input v-model="form.passport_number" label="Номер паспорта" type="number" outlined required />
          
          <q-btn type="submit" label="Зарегистрироваться" color="primary" class="full-width" />
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from "axios"
import { useQuasar } from 'quasar'
const $q = useQuasar()

const router = useRouter()
const form = ref({
  username: '',
  password: '',
  email: '',
  full_name: '',
  birth_date: '',
  passport_series: '',
  passport_number: ''
})
const register = async () => {
   const response = await axios.post('/api/auth/register/', {
      username: form.value.username,
      password: form.value.password,
      email: form.value.email || '',
      full_name: form.value.full_name,
      birth_date: form.value.birth_date,
      passport_series: form.value.passport_series.toString(),
      passport_number: form.value.passport_number.toString()
    })
    
    console.log('Ответ сервера:', response.data)
    
    if (response.data.success) {
      console.log("Регистрация успешна")
      
      // Сохраняем данные пользователя
      if (response.data.user) {
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('userId', response.data.user.id)
        localStorage.setItem('username', response.data.user.username)
      }
      
      // Показываем уведомление
      $q.notify({
        type: 'positive',
        message: 'Регистрация успешна!',
        timeout: 2000
      })
      } else {
      console.log("Ошибка регистрации")
    }
}
const handleRegister = async () => {
  const result = await register()
  
  if (result.success) {
    router.push('/')
  }
}
</script>