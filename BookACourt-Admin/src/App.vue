<script setup>
import HomeView from './views/HomeView.vue';
</script>

<template>
  <div>
    <Navbar />
    <RouterView />
    <Footer />
  </div>
</template>

<style scoped>
div {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>
