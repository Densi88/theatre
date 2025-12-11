<template>
    <div class="row q-col-gutter-md">
        <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="actor in actors" :key="actor.id">
            <div class="q-card q-ma-sm" @click="viewActorDetail(newsItem)">
                <q-img :src="getImage(actor.photo)" :ratio="16 / 9" />

                <div class="text-body1 text-weight-bold q-mt-sm">
                    {{ actor.name }}
                </div>

                <div class="text-body1 text-weight-medium q-mb-sm">
                    {{ actor.bio }}
                </div>
                <q-card-actions align="right">
                    <q-btn flat color="primary" icon="arrow_forward" label="Читать далее"
                        @click.stop="viewActorDetail(showItem)" />
                </q-card-actions>
            </div>
        </div>
    </div>

</template>


<script setup>
import axios from "axios"
const actors = ref([])
import { ref, onMounted } from 'vue'

const download = async () => {
    const response = await axios.get('/api/actors')
    actors.value = response.data
}

const getImage = (imagePath) => {
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    console.log('URL уже полный:', imagePath)
    return imagePath
  }

  return imagePath
}

onMounted(() => {
  download()
})

</script>