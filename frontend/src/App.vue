<template>
  <router-view />
</template>

<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'
const router = useRouter()
const userInfo=ref({})

router.afterEach(() => {
  getUserInfo()
})

const getUserInfo=async()=>{
  const data=await axios.get("/api/users/my/")
  userInfo.value=data.data
  console.log(userInfo)
}




onBeforeMount(() => {
  getUserInfo()
  updateCsrfToken()

  // axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>
