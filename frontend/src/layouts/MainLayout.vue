<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-2">
    <!-- Хедер -->
    <q-header elevated class="bg-grey-9 text-white">
      <q-toolbar>
        <q-btn flat to="/">
          <img src="theatre_logo.jpg" height="105"  />
        </q-btn>
        <q-toolbar-title>Театр</q-toolbar-title>
        <q-btn flat label="Главная" to="/" />
        <q-btn flat label="Спектакли" to="/shows" />
        <q-btn flat label="Новости" to="/news" />
        <q-btn flat label="Мои билеты" to="/my-tickets" />
        <q-btn flat label="Войти" to="/login" />
        <q-btn flat label="Купить билеты" to="/buy-tickets"></q-btn>
        <q-btn flat label="Админка" href="http://localhost:8000/admin/" target="_blank" />
      </q-toolbar>
    </q-header>

    <!-- Основной контент -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Футер -->
    <q-footer elevated class="bg-grey-9 text-white">
      <q-toolbar>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>
</script>

<style>

</style>
