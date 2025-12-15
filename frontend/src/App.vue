<template>
  <router-view />
</template>

<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
const userInfo=ref({})

const getUserInfo=async()=>{
  const data=await axios.get("/api/users/my/")
  userInfo.value=data.data
  console.log(userInfo)
}




onBeforeMount(() => {
  getUserInfo()

  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>
