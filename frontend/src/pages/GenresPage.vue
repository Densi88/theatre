<template>
    <div class="row q-col-gutter-md">
        <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="genre in genres" :key="genre.id">
            <div class="q-card q-ma-sm" @click="viewActorDetail(newsItem)">
                <div class="text-body1 text-weight-bold q-mt-sm">
                    {{ genre.genre_name }}
                </div>

                <div class="text-body1 text-weight-medium q-mb-sm">
                    {{ genre.description }}
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
const genres = ref([])
import { ref, onMounted } from 'vue'

const download = async () => {
    const response = await axios.get('/api/genres')
    genres.value = response.data
}
onMounted(() => {
  download()
})

</script>