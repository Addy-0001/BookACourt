<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <!-- Header -->
        <header class="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
            <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
                <button @click="goBack"
                    class="flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    <span class="font-medium">Back</span>
                </button>
                <h1 class="text-2xl font-bold text-slate-900">My Profile</h1>
                <button @click="handleLogout"
                    class="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg transition-colors font-medium">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    <span>Logout</span>
                </button>
            </div>
        </header>

        <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Loading State -->
            <div v-if="pageLoading" class="flex items-center justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <template v-else>
                <!-- Profile Hero Section -->
                <div class="bg-white rounded-xl shadow-md p-8 mb-8">
                    <div class="flex items-start gap-6">
                        <div class="relative">
                            <div
                                class="w-24 h-24 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-3xl font-bold overflow-hidden">
                                <img v-if="user.profile_picture" :src="user.profile_picture" alt="Profile"
                                    class="w-full h-full object-cover" />
                                <span v-else>{{ user.full_name?.charAt(0).toUpperCase() }}</span>
                            </div>
                            <button @click="editMode = true"
                                class="absolute bottom-0 right-0 bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full shadow-lg transition-colors">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                            </button>
                        </div>
                        <div>
                            <h2 class="text-3xl font-bold text-slate-900">{{ user.full_name }}</h2>
                            <span :class="['inline-block mt-2 px-3 py-1 rounded-full text-sm font-medium', roleClass]">
                                {{ roleDisplay }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Player Stats (if applicable) -->
                <div v-if="user.role === 'PLAYER' && stats"
                    class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-600">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-slate-600 text-sm font-medium">Total Bookings</p>
                                <p class="text-3xl font-bold text-slate-900 mt-1">{{ stats.total_bookings || 0 }}</p>
                            </div>
                            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-amber-600">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-slate-600 text-sm font-medium">Loyalty Points</p>
                                <p class="text-3xl font-bold text-slate-900 mt-1">{{ user.loyalty_points || 0 }}</p>
                            </div>
                            <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-amber-600" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-600">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-slate-600 text-sm font-medium">Matches Played</p>
                                <p class="text-3xl font-bold text-slate-900 mt-1">{{ stats.total_matches_played || 0 }}
                                </p>
                            </div>
                            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-purple-600">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-slate-600 text-sm font-medium">Rating</p>
                                <p class="text-3xl font-bold text-slate-900 mt-1">{{
                                    stats.sportsmanship_rating?.toFixed(1) || '5.0' }}/5.0</p>
                            </div>
                            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Personal Information Section -->
                <div class="bg-white rounded-xl shadow-md p-8 mb-8">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-xl font-bold text-slate-900">Personal Information</h3>
                        <button v-if="!editMode" @click="editMode = true"
                            class="flex items-center gap-2 px-3 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors font-medium">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                            Edit
                        </button>
                    </div>

                    <div v-if="successMessage"
                        class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-start gap-3">
                        <svg class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" fill="currentColor"
                            viewBox="0 0 20 20">
                            <path fill-rule="evenodd"
                                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                clip-rule="evenodd" />
                        </svg>
                        <p class="text-green-800 font-medium">{{ successMessage }}</p>
                    </div>

                    <div v-if="errorMessage"
                        class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                        <svg class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd"
                                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 001.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                clip-rule="evenodd" />
                        </svg>
                        <p class="text-red-800 font-medium">{{ errorMessage }}</p>
                    </div>

                    <form @submit.prevent="handleUpdateProfile" class="space-y-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-2">Full Name</label>
                                <input v-model="profileForm.full_name" type="text" :disabled="!editMode" required
                                    class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-slate-50 disabled:text-slate-500 transition-colors" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-2">Phone Number</label>
                                <input v-model="user.phone_number" type="tel" disabled
                                    class="w-full px-4 py-2 border border-slate-300 rounded-lg bg-slate-50 text-slate-500" />
                                <p class="text-xs text-slate-500 mt-1">Phone number cannot be changed</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-2">Email</label>
                                <input v-model="profileForm.email" type="email" :disabled="!editMode"
                                    class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-slate-50 disabled:text-slate-500 transition-colors" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-2">Date of Birth</label>
                                <input v-model="profileForm.date_of_birth" type="date" :disabled="!editMode"
                                    class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-slate-50 disabled:text-slate-500 transition-colors" />
                            </div>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-2">City</label>
                            <input v-model="profileForm.city" type="text" :disabled="!editMode" placeholder="Your city"
                                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-slate-50 disabled:text-slate-500 transition-colors" />
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-2">Address</label>
                            <textarea v-model="profileForm.address" :disabled="!editMode" rows="3"
                                placeholder="Your full address"
                                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-slate-50 disabled:text-slate-500 transition-colors resize-none" />
                        </div>

                        <div v-if="editMode" class="flex items-center justify-end gap-3 pt-4">
                            <button type="button" @click="cancelEdit"
                                class="px-6 py-2 border border-slate-300 text-slate-700 hover:bg-slate-50 rounded-lg transition-colors font-medium">
                                Cancel
                            </button>
                            <button type="submit" :disabled="loading"
                                class="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white rounded-lg transition-colors font-medium flex items-center gap-2">
                                <span v-if="loading">Saving...</span>
                                <span v-else>Save Changes</span>
                            </button>
                        </div>
                    </form>
                </div>

                <!-- Account Status Section -->
                <div class="bg-white rounded-xl shadow-md p-8">
                    <h3 class="text-xl font-bold text-slate-900 mb-6">Account Status</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="border border-slate-200 rounded-lg p-4">
                            <p class="text-sm font-medium text-slate-600">Account Created</p>
                            <p class="text-lg font-bold text-slate-900 mt-1">{{ formatDate(user.created_at) }}</p>
                        </div>
                        <div class="border border-slate-200 rounded-lg p-4">
                            <p class="text-sm font-medium text-slate-600">Phone Verified</p>
                            <div class="mt-1">
                                <span v-if="user.is_phone_verified"
                                    class="inline-flex items-center gap-1 px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd"
                                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                            clip-rule="evenodd" />
                                    </svg>
                                    Verified
                                </span>
                                <span v-else
                                    class="inline-flex items-center gap-1 px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-medium rounded-full">
                                    Not Verified
                                </span>
                            </div>
                        </div>
                        <div class="border border-slate-200 rounded-lg p-4">
                            <p class="text-sm font-medium text-slate-600">Account Status</p>
                            <div class="mt-1">
                                <span v-if="user.is_active"
                                    class="inline-flex items-center gap-1 px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd"
                                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                            clip-rule="evenodd" />
                                    </svg>
                                    Active
                                </span>
                                <span v-else
                                    class="inline-flex items-center gap-1 px-3 py-1 bg-red-100 text-red-800 text-sm font-medium rounded-full">
                                    Inactive
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authService } from '@/services/authService'
import apiClient from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const user = ref(authStore.user || {})
const stats = ref(null)

const editMode = ref(false)
const loading = ref(false)
const pageLoading = ref(true)
const successMessage = ref('')
const errorMessage = ref('')

const profileForm = ref({
    full_name: '',
    email: '',
    date_of_birth: '',
    city: '',
    address: '',
})

const roleClass = computed(() => {
    const roleMap = {
        'PLAYER': 'bg-blue-100 text-blue-800',
        'COURT_OWNER': 'bg-purple-100 text-purple-800',
        'COURT_MANAGER': 'bg-amber-100 text-amber-800',
        'SUPER_USER': 'bg-red-100 text-red-800'
    }
    return roleMap[user.value.role] || 'bg-blue-100 text-blue-800'
})

const roleDisplay = computed(() => {
    const roleMap = {
        'PLAYER': 'Player',
        'COURT_OWNER': 'Court Owner',
        'COURT_MANAGER': 'Court Manager',
        'SUPER_USER': 'Administrator'
    }
    return roleMap[user.value.role] || 'Player'
})

const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    })
}

const loadProfile = async () => {
    try {
        pageLoading.value = true
        const response = await apiClient.get('/user/profile/')
        user.value = response.data
        authStore.user = response.data

        // Initialize form with user data
        profileForm.value = {
            full_name: user.value.full_name || '',
            email: user.value.email || '',
            date_of_birth: user.value.date_of_birth || '',
            city: user.value.city || '',
            address: user.value.address || '',
        }

        // Load stats if player
        if (user.value.role === 'PLAYER') {
            await loadPlayerStats()
        }
    } catch (error) {
        console.error('Failed to load profile:', error)
        errorMessage.value = 'Failed to load profile data'
    } finally {
        pageLoading.value = false
    }
}

const loadPlayerStats = async () => {
    try {
        // Assuming there's an endpoint for player stats
        const response = await apiClient.get(`/user/profile/stats/`)
        stats.value = response.data
    } catch (error) {
        console.error('Failed to load stats:', error)
        // Stats are optional, so we don't show an error
    }
}

const handleUpdateProfile = async () => {
    loading.value = true
    successMessage.value = ''
    errorMessage.value = ''

    try {
        const response = await authService.updateProfile(profileForm.value)
        user.value = response
        successMessage.value = 'Profile updated successfully!'
        editMode.value = false

        setTimeout(() => {
            successMessage.value = ''
        }, 3000)
    } catch (error) {
        console.error('Update error:', error)
        errorMessage.value = error.response?.data?.detail || 'Failed to update profile'
        setTimeout(() => {
            errorMessage.value = ''
        }, 5000)
    } finally {
        loading.value = false
    }
}

const cancelEdit = () => {
    profileForm.value = {
        full_name: user.value.full_name || '',
        email: user.value.email || '',
        date_of_birth: user.value.date_of_birth || '',
        city: user.value.city || '',
        address: user.value.address || '',
    }
    editMode.value = false
    errorMessage.value = ''
}

const goBack = () => {
    router.go(-1)
}

const handleLogout = async () => {
    await authStore.logout()
    router.push('/login')
}

onMounted(() => {
    loadProfile()
})
</script>