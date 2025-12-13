<template>
    <div class="q-mb-md">
        <q-btn color="primary" icon="add" label="Добавить" @click="openAddDialog()" />
    </div>
    <div class="row q-col-gutter-md">
        <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="actorItem in actors" :key="actorItem.id">
            <div class="q-card q-ma-sm" @click="viewActorDetail(newsItem)">
                <q-img :src="getImage(actorItem.photo)" :ratio="16 / 9" />

                <div class="text-body1 text-weight-bold q-mt-sm">
                    {{ actorItem.name }}
                </div>

                <div class="text-body1 text-weight-medium q-mb-sm">
                    {{ actorItem.bio }}
                </div>
                <q-card-actions align="right">
                    <q-btn flat color="primary" icon="arrow_forward" label="Читать далее"
                        @click.stop="viewActorDetail(actorItem)" />
                </q-card-actions>
                <q-card-actions align="left">
                    <div class="q-mb-md">
                        <q-btn color="primary" icon="add" label="Удалить" @click.stop="deleteActor(actorItem)" />
                    </div>
                    <div class="q-mb-md">
                        <q-btn color="primary" icon="add" label="Изменить" @click.stop="openUpdateDialog(actorItem)" />
                    </div>
                </q-card-actions>
            </div>
        </div>
    </div>

    <q-dialog v-model="addDialog">
        <q-card style="min-width: 400px;">
            <q-card-section>
                <div class="text-h6">Добавить нового актера</div>
            </q-card-section>

            <q-card-section>
                <q-input v-model="newActor.name" label="ФИО" type="textarea" outlined class="q-mt-sm" />
                <q-input v-model="newActor.bio" label="Биография" type="textarea" class="q-mt-sm" />
                <q-file v-model="newActor.photo" label="Фотография" class="q-mt-sm" />
            </q-card-section>

            <q-card-actions align="right">
                <q-btn flat label="Отмена" color="negative" v-close-popup />
                <q-btn flat label="Добавить" color="primary" @click="submitAdd()" />
            </q-card-actions>
        </q-card>
    </q-dialog>

    <q-dialog v-model="updateDialog">
        <q-card style="min-width: 400px;">
            <q-card-section>
                <div class="text-h6">Редактировать актера</div>
            </q-card-section>

            <q-card-section>
                <q-input v-model="updatedActor.name" label="ФИО" type="textarea" outlined class="q-mt-sm" />
                <q-input v-model="updatedActor.bio" label="Биография" type="textarea" class="q-mt-sm" />
                <q-file v-model="updatedActor.photo" label="Фотография" class="q-mt-sm" />
            </q-card-section>

            <q-card-actions align="right">
                <q-btn flat label="Отмена" color="negative" v-close-popup />
                <q-btn flat label="Изменить" color="primary" @click="submitUpdate()" />
            </q-card-actions>
        </q-card>
    </q-dialog>


</template>


<script setup>
import axios from "axios"
const actors = ref([])
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'

const newActor=ref({
    name:'',
    bio:'',
    photo: null
})
const updatedActor=ref({
    id:'',
    name:'',
    bio:'',
    photo:null
})
const addDialog=ref(false)
const updateDialog=ref(false)
const $q = useQuasar()

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
const openAddDialog=()=>{
    addDialog.value=true
}
const submitAdd=async()=>{
     if (!newActor.value.name||!newActor.value.bio) {
        $q.notify({ type: 'warning', message: 'Заполните все поля' })
        return
    }

    try {
        const formData = new FormData()
        formData.append('name', newActor.value.name)
        formData.append('bio', newActor.value.bio)
        if(newActor.value.photo){
           formData.append('photo', newActor.value.photo) 
        }

        const response = await axios.post('/api/actors/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })

        $q.notify({ type: 'positive', message: 'Актер добавлен' })
        actors.value.push(response.data)
        addDialog.value = false
    } catch (error) {
        console.error(error)
        $q.notify({
            type: 'negative',
            message: 'Ошибка при добавлении',
            caption: error.response?.data || error.message
        })
    }
}
const deleteActor=async(actorItem)=>{
    try {
        const confirmDelete = window.confirm(`Удалить актера?`)
        if (!confirmDelete) return
        await axios.delete(`/api/actors/${actorItem.id}/`)

        actors.value = actors.value.filter(s => s.id !== actorItem.id)

        $q.notify({ type: 'positive', message: 'Новость удалена' })
    } catch (error) {
        console.error(error)
        $q.notify({
            type: 'negative',
            message: 'Ошибка при удалении',
            caption: error.response?.data || error.message
        })
    }
}
const openUpdateDialog=(actorItem)=>{
    updatedActor.value={id:actorItem.id, name: actorItem.name, bio: actorItem.bio, photo:actorItem.photo}
    updateDialog.value=true
}
const submitUpdate=async()=>{
  try {
        const formData = new FormData()
        formData.append('name', updatedActor.value.name)
        formData.append('bio', updatedActor.value.bio)
        if (updatedActor.value.photo instanceof File) {
            formData.append('photo', updatedActor.value.photo)
        }
        const response = await axios.patch(
            `/api/actors/${updatedActor.value.id}/`,
            formData  
        )
        console.log('Success!', response.data)
        $q.notify({ type: 'positive', message: 'Новость обновлена!' })
        await download()
        updateDialog.value = false
        
    } catch (error) {
        console.error('Full error:', error)
        console.error('Response data:', error.response?.data)
        $q.notify({
            type: 'negative',
            message: 'Ошибка обновления',
            caption: error.response?.data ? JSON.stringify(error.response.data) : error.message
        })
    }
}
onMounted(() => {
  download()
})

</script>