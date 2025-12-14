import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from 'boot/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const isAdmin = ref(false)

  // Инициализация из localStorage
  const init = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = JSON.parse(savedUser)
      isAuthenticated.value = true
      isAdmin.value = user.value.role === 'admin'
    }
  }

  // Логин
  const login = async (username, password) => {
    try {
      const response = await api.post('/api/auth/login/', {
        username,
        password
      }, {
        withCredentials: true  // Важно для сессий!
      })
      
      if (response.data.success) {
        user.value = response.data.user
        isAuthenticated.value = true
        isAdmin.value = user.value.role === 'admin'
        
        localStorage.setItem('user', JSON.stringify(response.data.user))
        return { success: true }
      } else {
        return { success: false, message: response.data.message }
      }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Ошибка сети' 
      }
    }
  }

  // Регистрация
  const register = async (userData) => {
    try {
      const response = await api.post('/api/auth/register/', userData, {
        withCredentials: true
      })
      
      if (response.data.success) {
        user.value = response.data.user
        isAuthenticated.value = true
        isAdmin.value = user.value.role === 'admin'
        
        localStorage.setItem('user', JSON.stringify(response.data.user))
        return { success: true }
      } else {
        return { success: false, message: response.data.message }
      }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Ошибка сети' 
      }
    }
  }

  // Выход
  const logout = async () => {
    try {
      await api.post('/api/auth/logout/', {}, {
        withCredentials: true
      })
    } catch (error) {
      console.error('Ошибка выхода:', error)
    } finally {
      user.value = null
      isAuthenticated.value = false
      isAdmin.value = false
      localStorage.removeItem('user')
    }
  }

  // Проверка авторизации
  const checkAuth = async () => {
    try {
      const response = await api.get('/api/auth/me/', {
        withCredentials: true
      })
      
      user.value = {
        ...response.data,
        role: response.data.role || 'user'
      }
      isAuthenticated.value = true
      isAdmin.value = user.value.role === 'admin'
      
      localStorage.setItem('user', JSON.stringify(user.value))
      return true
    } catch (error) {
      console.log(error)
      user.value = null
      isAuthenticated.value = false
      isAdmin.value = false
      localStorage.removeItem('user')
      return false
    }
  }

  return {
    user,
    isAuthenticated,
    isAdmin,
    init,
    login,
    register,
    logout,
    checkAuth
  }
})