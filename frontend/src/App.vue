<template>
  <router-view />
</template>

<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'
import { UseAuthStore } from 'src/stores/auth';
const authStore = UseAuthStore()
const router = useRouter()
const userInfo=ref({})

router.afterEach(() => {
  getUserInfo()
  authStore.updateCsrfToken()

})

const getUserInfo=async()=>{
  const data=await axios.get("/api/users/my/")
  userInfo.value=data.data
  console.log(userInfo)
}




onBeforeMount(() => {
  getUserInfo()

  // axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>
