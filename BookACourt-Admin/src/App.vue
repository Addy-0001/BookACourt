<script setup>
import HomeView from './views/HomeView.vue';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

<template>
  <div>
    <Navbar />
    <RouterView />
    <Footer />
  </div>
</template>

<style scoped>
*,
*::before,
*::after {
  padding: 0;
  margin: 0;
  font-weight: normal;
}


div {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>
