<template>
  <div id="app" class="min-h-screen flex flex-col">
    <!-- Navbar - shown on all pages except login/signup -->
    <Navbar v-if="showNavbar" />

    <!-- Main Content -->
    <main class="flex-1">
      <RouterView />
    </main>

    <!-- Footer - shown on all pages except login/signup -->
    <Footer v-if="showFooter" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/navbar.vue'
import Footer from './components/footer.vue'

const route = useRoute()

// Pages where we don't want to show navbar/footer
const guestPages = ['/login', '/signup']

const showNavbar = computed(() => {
  return !guestPages.includes(route.path)
})

const showFooter = computed(() => {
  return !guestPages.includes(route.path)
})
</script>

<style scoped>
/* Import base styles */
@import './assets/base.css';

/* Global styles */
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Focus styles for accessibility */
*:focus {
  outline: none;
}

*:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Loading states */
.loading-spinner {
  border: 3px solid #f3f4f6;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* Print styles */
@media print {

  nav,
  footer,
  .no-print {
    display: none !important;
  }
}
</style>