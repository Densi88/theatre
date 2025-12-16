import { defineStore } from 'pinia'
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';


export const UseAuthStore = defineStore("auth", () => {

    const username = ref();
    const is_authenticated = ref(null);
    const permissions = ref([])
    const is_staff=ref(null)

    async function fetchUserInfo() {
        const r = await axios.get("/api/users/my/");

        username.value = r.data.username;
        is_authenticated.value = r.data.is_authenticated;
        permissions.value = r.data.permissions;
        is_staff.value=r.data.is_staff;

    }
    const updateCsrfToken = () => {
        const csrfToken = Cookies.get('csrftoken')
        if (csrfToken) {
            axios.defaults.headers.common['X-CSRFToken'] = csrfToken
            console.log('CSRF token updated:', csrfToken)
        } else {
            console.warn('CSRF token not found in cookies')
        }
    }

    function hasPermission(name) {
        return permissions.value.includes(name);
    }

    onBeforeMount(async () => {
        fetchUserInfo();
        updateCsrfToken()
    })

    return {
        username,
        is_authenticated,
        is_staff,

        fetchUserInfo,
        hasPermission,
        updateCsrfToken,
    }

});