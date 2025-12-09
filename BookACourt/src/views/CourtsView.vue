<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Navigation -->
        <nav class="bg-white shadow-sm sticky top-0 z-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16">
                    <div class="flex items-center gap-4">
                        <button @click="goBack" class="text-gray-600 hover:text-gray-900">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 19l-7-7 7-7" />
                            </svg>
                        </button>
                        <h1 class="text-2xl font-bold text-blue-600">Courts</h1>
                    </div>
                    <div class="flex items-center gap-4">
                        <router-link to="/"
                            class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                            Home
                        </router-link>
                        <router-link to="/profile"
                            class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                            Profile
                        </router-link>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Content -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Search and Filters -->
            <div class="bg-white rounded-xl shadow-md p-6 mb-8">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="md:col-span-2">
                        <input v-model="searchQuery" type="text" placeholder="Search courts..."
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                    </div>
                    <select v-model="filterCity"
                        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="">All Cities</option>
                        <option value="Kathmandu">Kathmandu</option>
                        <option value="Bhaktapur">Bhaktapur</option>
                        <option value="Lalitpur">Lalitpur</option>
                    </select>
                    <select v-model="filterType"
                        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="">All Types</option>
                        <option value="Basketball">Basketball</option>
                        <option value="Badminton">Badminton</option>
                        <option value="Tennis">Tennis</option>
                        <option value="Futsal">Futsal</option>
                    </select>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <!-- Courts Grid -->
            <div v-else-if="courts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="court in filteredCourts" :key="court.id"
                    class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow cursor-pointer"
                    @click="viewCourtDetail(court.id)">
                    <div class="h-48 bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center">
                        <svg class="w-20 h-20 text-white opacity-50" fill="currentColor" viewBox="0 0 24 24">
                            <path
                                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
                        </svg>
                    </div>
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-2">
                            <h3 class="text-xl font-bold text-gray-900">{{ court.name }}</h3>
                            <span
                                class="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">Active</span>
                        </div>
                        <p class="text-gray-600 text-sm mb-4">{{ court.address }}</p>
                        <div class="flex items-center gap-4 text-sm text-gray-600 mb-4">
                            <div class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                                <span>{{ court.average_rating || '5.0' }}</span>
                            </div>
                            <span>•</span>
                            <span>{{ court.city }}</span>
                        </div>
                        <div class="flex items-center justify-between">
                            <span class="text-2xl font-bold text-blue-600">Rs {{ court.base_hourly_rate }}/hr</span>
                            <button @click.stop="bookCourt(court)"
                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                                Book Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-20">
                <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <p class="text-xl text-gray-600">No courts found</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

const router = useRouter()
const loading = ref(false)
const courts = ref([])
const searchQuery = ref('')
const filterCity = ref('')
const filterType = ref('')

const filteredCourts = computed(() => {
    return courts.value.filter(court => {
        const matchesSearch = court.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            court.address.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesCity = !filterCity.value || court.city === filterCity.value
        const matchesType = !filterType.value || court.court_type === filterType.value
        return matchesSearch && matchesCity && matchesType
    })
})

const loadCourts = async () => {
    loading.value = true
    try {
        // API endpoint to be implemented
        // const response = await apiClient.get('/courts/')
        // courts.value = response.data.results || response.data

        // Mock data for now
        courts.value = []
    } catch (error) {
        console.error('Failed to load courts:', error)
    } finally {
        loading.value = false
    }
}

const viewCourtDetail = (courtId) => {
    router.push(`/courts/${courtId}`)
}

const bookCourt = (court) => {
    router.push(`/courts/${court.id}`)
}

const goBack = () => {
    router.go(-1)
}

onMounted(() => {
    loadCourts()
})
</script>