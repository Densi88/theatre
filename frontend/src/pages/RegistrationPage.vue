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
import { useAuthStore } from 'stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: '',
  email: '',
  full_name: '',
  birth_date: '',
  passport_series: '',
  passport_number: ''
})

const handleRegister = async () => {
  const result = await authStore.register(form.value)
  
  if (result.success) {
    router.push('/')
  }
}
</script>