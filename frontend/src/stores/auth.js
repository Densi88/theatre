import { defineStore } from 'pinia'
import {ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';


export const UseAuthStore = defineStore("auth", () => {

    const username = ref();
    const is_authenticated = ref(null);
    const permissions = ref([])
    const is_staff=ref(null)
    const user_id=ref()
    const profile_id=ref()
    const isLoading = ref(false)

   const init = async () => {
        updateCsrfToken()
        await fetchUserInfo()
    }

    async function fetchUserInfo() {
        console.log('[AuthStore] Загрузка данных пользователя...')
        isLoading.value = true
        try {
            const r = await axios.get("/api/users/my/");
            console.log('[AuthStore] Ответ API:', r.data)
            
            user_id.value = r.data.id;
            username.value = r.data.username;
            is_authenticated.value = r.data.is_authenticated;
            permissions.value = r.data.permissions || [];
            is_staff.value = r.data.is_staff;
            profile_id.value = r.data.profile_id
            
            console.log('[AuthStore] После установки:', {
                is_authenticated: is_authenticated.value,
                profile_id: profile_id.value,
                username: username.value
            })
            
        } catch (error) {
            console.error('[AuthStore] Ошибка загрузки:', error)
            console.error('[AuthStore] Статус:', error.response?.status)
            console.error('[AuthStore] Данные ошибки:', error.response?.data)
            
            // Если 401 - не авторизован
            if (error.response?.status === 401) {
                is_authenticated.value = false
                username.value = ''
                profile_id.value = null
            }
        } finally {
            isLoading.value = false
        }
    }
    
    const updateCsrfToken = () => {
        const csrfToken = Cookies.get('csrftoken')
        if (csrfToken) {
            axios.defaults.headers.common['X-CSRFToken'] = csrfToken
            console.log('[AuthStore] CSRF token обновлен')
        } else {
            console.warn('[AuthStore] CSRF token не найден')
        }
    }

    function hasPermission(name) {
        return permissions.value.includes(name);
    }

    return {
        username,
        is_authenticated,
        is_staff,
        user_id,
        profile_id,
        isLoading,

        init,
        fetchUserInfo,
        hasPermission,
        updateCsrfToken,
    }

});