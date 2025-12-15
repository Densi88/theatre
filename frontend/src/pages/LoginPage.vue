<template>
    <q-page class="flex flex-center">
        <q-card style="width: 350px">
            <q-card-section>
                <div class="text-h6">Вход</div>
            </q-card-section>

            <q-card-section>
                <q-form class="q-gutter-md">
                    <q-input v-model="form.username" label="Логин" outlined :rules="[val => !!val || 'Обязательно']" />

                    <q-input v-model="form.password" label="Пароль" type="password" outlined
                        :rules="[val => !!val || 'Обязательно']" />

                    <q-btn type="submit" label="Войти" color="primary" class="full-width" />

                    <div class="text-center">
                        <q-btn flat label="Регистрация" @click="$router.push('/register')" />
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </q-page>
</template>

<script setup>


</script>