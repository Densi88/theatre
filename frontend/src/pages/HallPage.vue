<template>
  <div class="q-pa-md">
    <!-- Информация о сеансе -->
    <div class="row items-center q-mb-lg">
      <q-icon name="event_seat" size="md" color="primary" class="q-mr-sm" />
      <div>
        <div class="text-h4 text-weight-bold">Выбор мест</div>
        <div class="text-subtitle1 text-grey-7">
          {{ showTitle }} • {{ formatDate(sessionDate) }} • {{ sessionTime }}
        </div>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-if="error" class="q-pa-md bg-negative text-white rounded-borders q-mb-md">
      {{ error }}
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="text-center q-pa-xl">
      <q-spinner size="50px" color="primary" />
      <div class="q-mt-md text-subtitle1">Загрузка схемы зала...</div>
    </div>

    <!-- Основной контент -->
    <div v-else class="row q-col-gutter-lg">
      <!-- Левая часть: Схема зала -->
      <div class="col-12 col-md-8">
        <q-card class="q-pa-md">
          <!-- Сцена -->
          <div class="text-center q-mb-lg">
            <div class="stage">
              <div class="text-h6 text-weight-bold">СЦЕНА</div>
              <div class="text-caption text-grey">Экран/Сцена</div>
            </div>
          </div>

          <!-- Легенда -->
          <div class="row justify-center q-mb-md q-gutter-md">
            <div class="row items-center">
              <div class="seat-legend available"></div>
              <span class="q-ml-xs">Свободно</span>
            </div>
            <div class="row items-center">
              <div class="seat-legend selected"></div>
              <span class="q-ml-xs">Выбрано</span>
            </div>
            <div class="row items-center">
              <div class="seat-legend occupied"></div>
              <span class="q-ml-xs">Занято</span>
            </div>
          </div>

          <!-- Схема зала -->
          <div class="hall-layout q-mt-lg">
            <!-- Номера рядов слева -->
            <div class="row-numbers">
              <div 
                v-for="row in totalRows" 
                :key="'row-' + row"
                class="row-number"
              >
                {{ row }}
              </div>
            </div>

            <!-- Места -->
            <div class="seats-container">
              <div 
                v-for="row in seatsMatrix" 
                :key="'row-' + row[0].row"
                class="row"
              >
                <div 
                  v-for="seat in row" 
                  :key="'seat-' + seat.row + '-' + seat.seat"
                  :class="[
                    'seat',
                    getSeatClass(seat),
                    { 'aisle-left': seat.seat === Math.floor(totalSeatsPerRow / 2) },
                    { 'aisle-right': seat.seat === Math.floor(totalSeatsPerRow / 2) + 1 }
                  ]"
                  @click="toggleSeat(seat)"
                  :title="`Ряд ${seat.row}, Место ${seat.seat}`"
                >
                  <div class="seat-number">{{ seat.seat }}</div>
                </div>
              </div>
            </div>

            <!-- Номера рядов справа -->
            <div class="row-numbers">
              <div 
                v-for="row in totalRows" 
                :key="'row-right-' + row"
                class="row-number"
              >
                {{ row }}
              </div>
            </div>
          </div>

          <!-- Номера мест внизу -->
          <div class="seat-numbers">
            <div 
              v-for="seat in totalSeatsPerRow" 
              :key="'number-' + seat"
              class="seat-number-bottom"
            >
              {{ seat }}
            </div>
          </div>

          <!-- Инструкция -->
          <div class="text-center q-mt-lg text-caption text-grey">
            Кликните на место, чтобы выбрать/отменить
          </div>
        </q-card>
      </div>

      <!-- Правая часть: Информация и покупка -->
      <div class="col-12 col-md-4">
        <q-card class="sticky-card">
          <q-card-section>
            <div class="text-h6">Ваш заказ</div>
            <div class="text-subtitle2 text-grey-7 q-mb-md">
              Сеанс: {{ formatDate(sessionDate) }}, {{ sessionTime }}
            </div>

            <!-- Выбранные места -->
            <div v-if="selectedSeats.length === 0" class="text-center q-py-lg">
              <q-icon name="event_seat" size="40px" color="grey-4" />
              <div class="text-grey q-mt-sm">Выберите места на схеме</div>
            </div>

            <div v-else>
              <div class="text-subtitle1 q-mb-sm">Выбранные места:</div>
              <q-list bordered separator>
                <q-item 
                  v-for="seat in selectedSeats" 
                  :key="seat.row + '-' + seat.seat"
                >
                  <q-item-section>
                    <q-item-label>Ряд {{ seat.row }}, Место {{ seat.seat }}</q-item-label>
                    <q-item-label caption>
                      {{ getSeatPrice(seat) }} ₽
                    </q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-btn 
                      icon="close" 
                      size="sm" 
                      flat 
                      round 
                      @click="removeSeat(seat)"
                    />
                  </q-item-section>
                </q-item>
              </q-list>

              <!-- Итого -->
              <div class="q-mt-lg">
                <div class="row justify-between items-center q-pa-sm bg-grey-2 rounded-borders">
                  <div class="text-weight-medium">Итого:</div>
                  <div class="text-h6 text-primary">{{ totalPrice }} ₽</div>
                </div>
                <div class="text-caption text-grey q-mt-xs">
                  {{ selectedSeats.length }} мест
                </div>
              </div>
            </div>
          </q-card-section>

          <q-card-actions vertical>
            <!-- Кнопка покупки -->
            <q-btn
              color="primary"
              size="lg"
              :label="buyButtonLabel"
              :disabled="selectedSeats.length === 0 || buying"
              @click="buyTickets"
              class="q-mb-sm full-width"
            >
              <template v-if="buying" v-slot:loading>
                <q-spinner size="sm" />
              </template>
            </q-btn>

            <!-- Информация о зале -->
           
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'

const $q = useQuasar()
const route = useRoute()
const router = useRouter()

// Данные
const loading = ref(true)
const error = ref('')
const sessionData = ref(null)
const seatsMatrix = ref([])
const selectedSeats = ref([])
const buying = ref(false)

// Цены (можно получать из API или фиксированные)
const regularPrice = ref(1500)
// Параметры зала
const totalRows = computed(() => sessionData.value?.rows || 0)
const totalSeatsPerRow = computed(() => sessionData.value?.seats_per_row || 0)
const sessionDate = computed(() => sessionData.value?.date || '')
const sessionTime = computed(() => sessionData.value?.time || '')
const showTitle = computed(() => sessionData.value?.show_title || 'Спектакль')

// Загрузка схемы зала
const loadHallLayout = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const sessionId = route.params.id
    
    // Получаем схему мест для сеанса
    const response = await axios.get(`/api/sessions/${sessionId}/seats/`)
    sessionData.value = response.data
    seatsMatrix.value = response.data.seats_matrix || []
    
    console.log('Данные сеанса:', sessionData.value)
  } catch (err) {
    console.error('Ошибка загрузки:', err)
    error.value = 'Не удалось загрузить схему зала. Попробуйте позже.'
  } finally {
    loading.value = false
  }
}

// Форматирование даты
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    weekday: 'long',
    day: 'numeric',
    month: 'long'
  })
}

// Определение класса места
const getSeatClass = (seat) => {
  if (seat.occupied) return 'occupied'
  if (isSeatSelected(seat)) return 'selected'
  return 'available'
}
// Получение цены места
const getSeatPrice = () => {
  return  regularPrice.value
}

// Проверка выбора места
const isSeatSelected = (seat) => {
  return selectedSeats.value.some(s => 
    s.row === seat.row && s.seat === seat.seat
  )
}

// Выбор/отмена места
const toggleSeat = (seat) => {
  if (seat.occupied) {
    $q.notify({
      type: 'warning',
      message: 'Это место уже занято'
    })
    return
  }
  
  const index = selectedSeats.value.findIndex(s => 
    s.row === seat.row && s.seat === seat.seat
  )
  
  if (index >= 0) {
    // Удаляем из выбранных
    selectedSeats.value.splice(index, 1)
  } else {
    // Добавляем в выбранные
    selectedSeats.value.push({
      row: seat.row,
      seat: seat.seat,
      price: getSeatPrice(seat)
    })
  }
}

// Удалить конкретное место
const removeSeat = (seatToRemove) => {
  selectedSeats.value = selectedSeats.value.filter(seat => 
    !(seat.row === seatToRemove.row && seat.seat === seatToRemove.seat)
  )
}

// Итоговая цена
const totalPrice = computed(() => {
  return selectedSeats.value.reduce((sum, seat) => {
    return sum + (seat.price || regularPrice.value)
  }, 0)
})

// Текст кнопки покупки
const buyButtonLabel = computed(() => {
  if (buying.value) return 'Обработка...'
  if (selectedSeats.value.length === 0) return 'Выберите места'
  return `Купить ${selectedSeats.value.length} билет${selectedSeats.value.length > 1 ? 'а' : ''}`
})

// Покупка билетов
const buyTickets = async () => {
  if (selectedSeats.value.length === 0) return
  
  buying.value = true
  
  try {
    // Получаем ID текущего пользователя (обычно из store/auth)
    const userId = localStorage.getItem('userId') || 1 // Замените на реальный ID
    
    // Создаем билеты для каждого выбранного места
    const promises = selectedSeats.value.map(seat => {
      const ticketData = {
        show: sessionData.value.show_id || route.params.showId,
        session: route.params.id,
        row: seat.row,
        seat: seat.seat,
        price: seat.price,
        user: userId
      }
      console.log('Отправляю данные билета:', ticketData)
      
      return axios.post('/api/tickets/', ticketData)
    })
    
    // Отправляем все запросы
    await Promise.all(promises)
    
    // Успешная покупка
    $q.notify({
      type: 'positive',
      message: `Билеты успешно куплены! Сумма: ${totalPrice.value} ₽`,
      timeout: 5000
    })
    
    // Переход к билетам или на главную
    setTimeout(() => {
      router.push('/my-tickets') // или '/profile/tickets'
    }, 2000)
    
  } catch (err) {
    console.error('Ошибка покупки:', err)
    
    // Проверяем, какие места уже заняли
    if (err.response?.data?.error?.includes('Место уже занято')) {
      error.value = 'Некоторые места уже заняты. Обновите схему и выберите другие места.'
      // Перезагружаем схему
      await loadHallLayout()
    } else {
      $q.notify({
        type: 'negative',
        message: 'Ошибка покупки. Попробуйте снова.'
      })
    }
  } finally {
    buying.value = false
  }
}

// Инициализация
onMounted(() => {
  loadHallLayout()
})
</script>

<style scoped>
/* Легенда */
.seat-legend {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  margin-right: 5px;
}

.seat-legend.available { background: #4CAF50; }
.seat-legend.selected { background: #2196F3; }
.seat-legend.occupied { background: #F44336; }
.seat-legend.vip { background: #FF9800; }

/* Схема зала */
.hall-layout {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin: 20px 0;
}

.row-numbers {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 100%;
  padding-right: 15px;
}

.row-number {
  width: 30px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #666;
}

.seats-container {
  flex-grow: 1;
}

.row {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.seat {
  width: 40px;
  height: 40px;
  margin: 2px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  transition: all 0.2s;
  position: relative;
}

.seat:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.seat-number {
  pointer-events: none;
}

/* Цвета мест */
.seat.available {
  background: #4CAF50;
  color: white;
}

.seat.selected {
  background: #2196F3;
  color: white;
}

.seat.occupied {
  background: #F44336;
  color: white;
  cursor: not-allowed;
}

.seat.vip {
  background: #FF9800;
  color: white;
}

/* Проходы */
.aisle-left {
  margin-right: 20px;
  position: relative;
}

.aisle-right {
  margin-left: 20px;
  position: relative;
}

.aisle-left::after,
.aisle-right::before {
  content: '';
  position: absolute;
  top: 0;
  width: 20px;
  height: 100%;
  background: #f5f5f5;
}

.aisle-left::after {
  right: -20px;
}

.aisle-right::before {
  left: -20px;
}

/* Номера мест внизу */
.seat-numbers {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.seat-number-bottom {
  width: 40px;
  text-align: center;
  font-size: 11px;
  color: #666;
  margin: 0 2px;
}

/* Стики карточка */
.sticky-card {
  position: sticky;
  top: 20px;
}

@media (max-width: 768px) {
  .seat {
    width: 30px;
    height: 30px;
    font-size: 10px;
  }
  
  .row-number {
    width: 20px;
    height: 30px;
    font-size: 12px;
  }
  
  .aisle-left {
    margin-right: 15px;
  }
  
  .aisle-right {
    margin-left: 15px;
  }
}
</style>