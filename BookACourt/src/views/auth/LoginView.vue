<!-- views/auth/LoginView.vue -->
<template>
  <div
    class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo / Brand (optional - can be removed or customized) -->
      <div class="text-center mb-10">
        <div class="inline-block">
          <span class="text-4xl font-black bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
            BookACourt
          </span>
        </div>
        <p class="mt-2 text-gray-600 font-medium">Reserve your court in seconds</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white rounded-2xl shadow-2xl border border-emerald-100 overflow-hidden">
        <div class="p-8 md:p-10">
          <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
            <p class="text-gray-600">Log in to continue booking your favorite courts</p>
          </div>

          <!-- Error Message -->
          <div v-if="error"
            class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-center gap-3">
            <svg class="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ error }}</span>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-6">
            <!-- Phone Number -->
            <div class="space-y-2">
              <label for="phone" class="block text-sm font-semibold text-gray-700">Phone Number</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
                  <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
                <input id="phone" v-model="loginForm.phone_number" type="tel" placeholder="+977 9800000000" required
                  class="w-full pl-12 pr-4 py-3.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all" />
              </div>
            </div>

            <!-- Password -->
            <div class="space-y-2">
              <label for="password" class="block text-sm font-semibold text-gray-700">Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
                  <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                    <path d="M7 11V7a5 5 0 0110 0v4" />
                  </svg>
                </div>

                <input id="password" v-model="loginForm.password" :type="showPassword ? 'text' : 'password'"
                  placeholder="••••••••" required
                  class="w-full pl-12 pr-12 py-3.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all" />

                <button type="button"
                  class="absolute inset-y-0 right-0 flex items-center pr-4 text-gray-500 hover:text-emerald-600 transition-colors"
                  @click="showPassword = !showPassword">
                  <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Submit Button -->
            <button type="submit" :disabled="loading"
              class="w-full py-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all disabled:opacity-60 disabled:cursor-not-allowed mt-4">
              {{ loading ? 'Logging in...' : 'Login' }}
            </button>

            <!-- Footer Links -->
            <div class="text-center mt-6 text-gray-600">
              <p>
                Don't have an account?
                <router-link to="/signup"
                  class="text-emerald-700 font-semibold hover:text-emerald-800 transition-colors">
                  Sign up
                </router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loginForm = ref({
  phone_number: '',
  password: '',
})

const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(loginForm.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Invalid phone number or password'
  } finally {
    loading.value = false
  }
}
</script>