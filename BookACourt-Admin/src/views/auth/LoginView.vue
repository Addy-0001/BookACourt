<!-- views/auth/LoginView.vue -->
<template>
    <div
        class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center p-4">
        <div class="w-full max-w-md">
            <!-- Branding -->
            <div class="text-center mb-10">
                <div class="inline-flex items-center gap-4 mb-4">
                    <div
                        class="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-600 to-teal-600 flex items-center justify-center text-white text-4xl shadow-xl">
                        🏟️
                    </div>
                    <div class="text-left">
                        <h1
                            class="text-4xl font-extrabold bg-gradient-to-r from-emerald-700 to-teal-700 bg-clip-text text-transparent">
                            Court Manager
                        </h1>
                        <p class="text-base text-emerald-800 font-medium mt-1">Manage Venues • Bookings • Revenue</p>
                    </div>
                </div>
            </div>

            <!-- Login Card -->
            <div class="bg-white rounded-3xl shadow-2xl border border-emerald-100/50 overflow-hidden">
                <div class="p-10 md:p-12">
                    <div class="text-center mb-10">
                        <h2 class="text-3xl font-bold text-gray-900 mb-3">Sign In</h2>
                        <p class="text-gray-600">Access your venue management dashboard</p>
                    </div>

                    <!-- Error -->
                    <div v-if="errorMessage"
                        class="mb-8 p-5 bg-red-50 border border-red-200 rounded-2xl text-red-800 flex items-center gap-4">
                        <svg class="w-7 h-7 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        <span class="text-base">{{ errorMessage }}</span>
                    </div>

                    <form @submit.prevent="handleLogin" class="space-y-7">
                        <!-- Phone -->
                        <div class="space-y-2">
                            <label for="phone" class="block text-base font-semibold text-gray-800">Phone Number</label>
                            <div class="relative">
                                <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                                    <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                    </svg>
                                </div>
                                <input id="phone" v-model="loginForm.phone_number" type="tel"
                                    placeholder="+977 9812345678" required :disabled="loading"
                                    class="w-full pl-14 pr-5 py-4 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all text-lg disabled:bg-gray-50 disabled:cursor-not-allowed" />
                            </div>
                        </div>

                        <!-- Password -->
                        <div class="space-y-2">
                            <label for="password" class="block text-base font-semibold text-gray-800">Password</label>
                            <div class="relative">
                                <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                                    <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                                        <path d="M7 11V7a5 5 0 0110 0v4" />
                                    </svg>
                                </div>

                                <input id="password" v-model="loginForm.password"
                                    :type="showPassword ? 'text' : 'password'" placeholder="••••••••••••" required
                                    :disabled="loading"
                                    class="w-full pl-14 pr-14 py-4 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all text-lg disabled:bg-gray-50 disabled:cursor-not-allowed" />

                                <button type="button" @click="showPassword = !showPassword"
                                    class="absolute inset-y-0 right-0 pr-5 flex items-center text-gray-500 hover:text-emerald-700 transition-colors">
                                    <svg v-if="showPassword" class="w-6 h-6" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                                        <circle cx="12" cy="12" r="3" />
                                    </svg>
                                    <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path
                                            d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" />
                                        <line x1="1" y1="1" x2="23" y2="23" />
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <!-- Remember + Forgot -->
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-sm mt-2">
                            <label class="flex items-center gap-3 cursor-pointer">
                                <input v-model="rememberMe" type="checkbox"
                                    class="w-5 h-5 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500" />
                                <span class="text-gray-700 font-medium">Remember me</span>
                            </label>

                            <router-link to="/forgot-password"
                                class="text-emerald-700 hover:text-emerald-800 font-medium transition-colors hover:underline">
                                Forgot password?
                            </router-link>
                        </div>

                        <!-- Submit -->
                        <button type="submit" :disabled="loading"
                            class="w-full mt-8 py-5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-2xl font-bold shadow-lg hover:shadow-xl transition-all disabled:opacity-60 disabled:cursor-not-allowed text-lg flex items-center justify-center gap-3">
                            <svg v-if="loading" class="animate-spin h-6 w-6 text-white"
                                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4" />
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                            </svg>
                            <span>{{ loading ? 'Signing in...' : 'Sign In' }}</span>
                        </button>
                    </form>

                    <!-- Footer -->
                    <div class="mt-12 text-center text-gray-600 text-sm">
                        <p>Need help managing your courts?</p>
                        <p class="mt-2">
                            Contact support:
                            <a href="mailto:support@bookacourt.com"
                                class="text-emerald-700 hover:text-emerald-800 font-medium hover:underline">
                                support@bookacourt.com
                            </a>
                        </p>
                    </div>
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

const rememberMe = ref(true)
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
    loading.value = true
    errorMessage.value = ''

    try {
        await authStore.login(loginForm.value)
        // Redirect to your main admin dashboard (change as needed)
        router.push('/dashboard') // ← Simple, clean route
    } catch (err) {
        errorMessage.value = err.response?.data?.detail || 'Invalid phone number or password. Please try again.'
    } finally {
        loading.value = false
    }
}
</script>