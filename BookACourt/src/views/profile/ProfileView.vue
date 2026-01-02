<template>
    <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <!-- Loading State -->
            <div v-if="pageLoading" class="flex items-center justify-center py-32">
                <div class="w-14 h-14 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
            </div>

            <template v-else>
                <!-- Profile Hero Card -->
                <div class="bg-white rounded-2xl shadow-xl border border-emerald-100 overflow-hidden mb-10">
                    <div class="p-8 md:p-10">
                        <div class="flex flex-col md:flex-row items-start md:items-center gap-8">
                            <!-- Avatar -->
                            <div class="relative group">
                                <div
                                    class="w-32 h-32 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white text-4xl font-bold overflow-hidden shadow-lg ring-4 ring-emerald-100">
                                    <img v-if="user.profile_picture" :src="user.profile_picture" alt="Profile Picture"
                                        class="w-full h-full object-cover transition-transform group-hover:scale-105 duration-300" />
                                    <span v-else>{{ user.full_name?.charAt(0).toUpperCase() || '?' }}</span>
                                </div>

                                <!-- Edit photo button -->
                                <button @click="$refs.fileInput.click()" :disabled="uploadingImage"
                                    class="absolute bottom-2 right-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-gray-400 text-white p-3 rounded-full shadow-lg transition-all transform hover:scale-110">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                                    </svg>
                                </button>

                                <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*"
                                    class="hidden" />
                            </div>

                            <!-- Info -->
                            <div class="flex-1">
                                <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                                    <div>
                                        <h2 class="text-3xl md:text-4xl font-bold text-gray-900">{{ user.full_name ||
                                            'User' }}</h2>
                                        <span :class="[
                                            'inline-block mt-3 px-4 py-1.5 rounded-full text-sm font-semibold',
                                            roleClass
                                        ]">
                                            {{ roleDisplay }}
                                        </span>
                                    </div>

                                    <!-- Remove photo button (only if exists) -->
                                    <button v-if="user.profile_picture" @click="handleRemoveProfilePicture"
                                        :disabled="uploadingImage"
                                        class="px-5 py-2.5 bg-red-50 hover:bg-red-100 text-red-700 rounded-lg font-medium transition-colors flex items-center gap-2 disabled:opacity-50">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                        Remove Photo
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Player Stats Cards (for players) -->
                <div v-if="user.role === 'PLAYER' && stats"
                    class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                    <div
                        class="bg-white rounded-2xl shadow-md p-6 border-t-4 border-emerald-600 hover:shadow-lg transition-shadow">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm font-medium text-gray-600">Total Bookings</p>
                                <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.total_bookings || 0 }}</p>
                            </div>
                            <div class="w-14 h-14 bg-emerald-100 rounded-xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-emerald-600" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div
                        class="bg-white rounded-2xl shadow-md p-6 border-t-4 border-amber-600 hover:shadow-lg transition-shadow">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm font-medium text-gray-600">Loyalty Points</p>
                                <p class="text-3xl font-bold text-gray-900 mt-2">{{ user.loyalty_points || 0 }}</p>
                            </div>
                            <div class="w-14 h-14 bg-amber-100 rounded-xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-amber-600" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div
                        class="bg-white rounded-2xl shadow-md p-6 border-t-4 border-teal-600 hover:shadow-lg transition-shadow">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm font-medium text-gray-600">Matches Played</p>
                                <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.total_matches_played || 0 }}
                                </p>
                            </div>
                            <div class="w-14 h-14 bg-teal-100 rounded-xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-teal-600" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Personal Information -->
                <div class="bg-white rounded-2xl shadow-xl border border-emerald-100 p-8 md:p-10 mb-10">
                    <div class="flex items-center justify-between mb-8">
                        <h3 class="text-2xl font-bold text-gray-900">Personal Information</h3>

                        <button v-if="!editMode" @click="editMode = true"
                            class="flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium transition-colors">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                            Edit Profile
                        </button>
                    </div>

                    <!-- Success / Error Messages -->
                    <div v-if="successMessage"
                        class="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 font-medium flex items-center gap-3">
                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd"
                                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                clip-rule="evenodd" />
                        </svg>
                        {{ successMessage }}
                    </div>

                    <div v-if="errorMessage"
                        class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-800 font-medium flex items-center gap-3">
                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd"
                                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                clip-rule="evenodd" />
                        </svg>
                        {{ errorMessage }}
                    </div>

                    <!-- Form -->
                    <form v-if="editMode" @submit.prevent="handleUpdateProfile" class="space-y-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="space-y-2">
                                <label class="block text-sm font-semibold text-gray-700">Full Name</label>
                                <input v-model="profileForm.full_name" type="text" required
                                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent" />
                            </div>

                            <div class="space-y-2">
                                <label class="block text-sm font-semibold text-gray-700">Email</label>
                                <input v-model="profileForm.email" type="email" disabled
                                    class="w-full px-4 py-3 border border-gray-300 rounded-xl bg-gray-50 cursor-not-allowed" />
                            </div>

                            <div class="space-y-2">
                                <label class="block text-sm font-semibold text-gray-700">Date of Birth</label>
                                <input v-model="profileForm.date_of_birth" type="date"
                                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent" />
                            </div>

                            <div class="space-y-2">
                                <label class="block text-sm font-semibold text-gray-700">City</label>
                                <input v-model="profileForm.city" type="text"
                                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent" />
                            </div>

                            <div class="md:col-span-2 space-y-2">
                                <label class="block text-sm font-semibold text-gray-700">Address</label>
                                <textarea v-model="profileForm.address" rows="3"
                                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent"></textarea>
                            </div>
                        </div>

                        <div class="flex flex-col sm:flex-row gap-4 pt-4">
                            <button type="submit" :disabled="loading"
                                class="px-8 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-md hover:shadow-lg transition-all disabled:opacity-50">
                                {{ loading ? 'Saving...' : 'Save Changes' }}
                            </button>

                            <button type="button" @click="cancelEdit"
                                class="px-8 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-xl font-medium transition-colors">
                                Cancel
                            </button>
                        </div>
                    </form>

                    <!-- Display mode -->
                    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div>
                            <p class="text-sm font-semibold text-gray-600">Full Name</p>
                            <p class="mt-2 text-lg font-medium text-gray-900">{{ user.full_name || '—' }}</p>
                        </div>

                        <div>
                            <p class="text-sm font-semibold text-gray-600">Email</p>
                            <p class="mt-2 text-lg font-medium text-gray-900">{{ user.email || '—' }}</p>
                        </div>

                        <div>
                            <p class="text-sm font-semibold text-gray-600">Date of Birth</p>
                            <p class="mt-2 text-lg font-medium text-gray-900">{{ user.date_of_birth ?
                                formatDate(user.date_of_birth) : '—' }}</p>
                        </div>

                        <div>
                            <p class="text-sm font-semibold text-gray-600">City</p>
                            <p class="mt-2 text-lg font-medium text-gray-900">{{ user.city || '—' }}</p>
                        </div>

                        <div class="md:col-span-2">
                            <p class="text-sm font-semibold text-gray-600">Address</p>
                            <p class="mt-2 text-lg font-medium text-gray-900">{{ user.address || '—' }}</p>
                        </div>
                    </div>
                </div>

                <!-- Account Status -->
                <div class="bg-white rounded-2xl shadow-xl border border-emerald-100 p-8 md:p-10">
                    <h3 class="text-2xl font-bold text-gray-900 mb-8">Account Status</h3>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="p-6 bg-gray-50 rounded-xl border border-gray-200">
                            <p class="text-sm font-medium text-gray-600">Account Created</p>
                            <p class="mt-3 text-xl font-bold text-gray-900">{{ formatDate(user.created_at) }}</p>
                        </div>

                        <div class="p-6 bg-gray-50 rounded-xl border border-gray-200">
                            <p class="text-sm font-medium text-gray-600">Phone Verified</p>
                            <div class="mt-3">
                                <span v-if="user.is_phone_verified"
                                    class="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-100 text-emerald-800 font-medium rounded-full">
                                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd"
                                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                            clip-rule="evenodd" />
                                    </svg>
                                    Verified
                                </span>
                                <span v-else
                                    class="inline-flex items-center gap-2 px-4 py-1.5 bg-yellow-100 text-yellow-800 font-medium rounded-full">
                                    Not Verified
                                </span>
                            </div>
                        </div>

                        <div class="p-6 bg-gray-50 rounded-xl border border-gray-200">
                            <p class="text-sm font-medium text-gray-600">Account Status</p>
                            <div class="mt-3">
                                <span v-if="user.is_active"
                                    class="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-100 text-emerald-800 font-medium rounded-full">
                                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd"
                                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                            clip-rule="evenodd" />
                                    </svg>
                                    Active
                                </span>
                                <span v-else
                                    class="inline-flex items-center gap-2 px-4 py-1.5 bg-red-100 text-red-800 font-medium rounded-full">
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
const fileInput = ref(null)
const uploadingImage = ref(false)

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
        const response = await apiClient.get(`/users/player-stats/me/`)
        stats.value = response.data
    } catch (error) {
        console.error('Failed to load stats:', error)
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

const handleFileSelect = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if (!allowedTypes.includes(file.type)) {
        errorMessage.value = 'Please select a valid image file (JPEG, PNG, or WebP)'
        setTimeout(() => {
            errorMessage.value = ''
        }, 5000)
        return
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
        errorMessage.value = 'Image size must be less than 5MB'
        setTimeout(() => {
            errorMessage.value = ''
        }, 5000)
        return
    }

    uploadingImage.value = true
    successMessage.value = ''
    errorMessage.value = ''

    try {
        const formData = new FormData()
        formData.append('profile_picture', file)

        const response = await apiClient.patch('/user/profile/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })

        user.value = response.data
        authStore.user = response.data
        successMessage.value = 'Profile picture updated successfully!'

        setTimeout(() => {
            successMessage.value = ''
        }, 3000)
    } catch (error) {
        console.error('Upload error:', error)
        errorMessage.value = error.response?.data?.detail || 'Failed to upload profile picture'
        setTimeout(() => {
            errorMessage.value = ''
        }, 5000)
    } finally {
        uploadingImage.value = false
        if (fileInput.value) {
            fileInput.value.value = ''
        }
    }
}

const handleRemoveProfilePicture = async () => {
    if (!confirm('Are you sure you want to remove your profile picture?')) {
        return
    }

    uploadingImage.value = true
    successMessage.value = ''
    errorMessage.value = ''

    try {
        const response = await apiClient.patch('/user/profile/', {
            profile_picture: null
        })

        user.value = response.data
        authStore.user = response.data
        successMessage.value = 'Profile picture removed successfully!'

        setTimeout(() => {
            successMessage.value = ''
        }, 3000)
    } catch (error) {
        console.error('Remove error:', error)
        errorMessage.value = error.response?.data?.detail || 'Failed to remove profile picture'
        setTimeout(() => {
            errorMessage.value = ''
        }, 5000)
    } finally {
        uploadingImage.value = false
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