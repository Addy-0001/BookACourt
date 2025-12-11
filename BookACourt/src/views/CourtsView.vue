<template>
    <div class="min-h-screen bg-gray-50">
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
                        <option v-for="city in uniqueCities" :key="city" :value="city">{{ city }}</option>
                    </select>
                    <select v-model="filterCategory"
                        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="">All Categories</option>
                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                    </select>
                </div>
                <div class="mt-4 flex items-center gap-4">
                    <label class="flex items-center gap-2">
                        <input v-model="filterIndoor" type="checkbox" class="rounded text-blue-600" />
                        <span class="text-sm">Indoor Only</span>
                    </label>
                    <div class="flex items-center gap-2">
                        <label class="text-sm">Max Price:</label>
                        <input v-model.number="maxPrice" type="number" min="0" placeholder="Any"
                            class="w-32 px-3 py-1 border border-gray-300 rounded-lg text-sm" />
                    </div>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="text-center py-20">
                <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-xl text-gray-600 mb-4">{{ error }}</p>
                <button @click="loadCourts" class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Try Again
                </button>
            </div>

            <!-- Courts Grid -->
            <div v-else-if="filteredCourts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="court in filteredCourts" :key="court.id"
                    class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow cursor-pointer"
                    @click="viewCourtDetail(court.id)">
                    <div v-if="court.primary_image" class="h-48 overflow-hidden">
                        <img :src="court.primary_image" :alt="court.name" class="w-full h-full object-cover" />
                    </div>
                    <div v-else
                        class="h-48 bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center">
                        <svg class="w-20 h-20 text-white opacity-50" fill="currentColor" viewBox="0 0 24 24">
                            <path
                                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
                        </svg>
                    </div>
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-2">
                            <h3 class="text-xl font-bold text-gray-900">{{ court.name }}</h3>
                            <span v-if="court.is_verified"
                                class="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">Verified</span>
                        </div>
                        <p class="text-gray-600 text-sm mb-2">{{ court.category_name || court.court_type }}</p>
                        <p class="text-gray-500 text-sm mb-4">{{ court.city }}</p>
                        <div class="flex items-center gap-4 text-sm text-gray-600 mb-4">
                            <div class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                                <span>{{ court.average_rating || '0.0' }} ({{ court.total_reviews || 0 }})</span>
                            </div>
                            <span v-if="court.is_indoor">•</span>
                            <span v-if="court.is_indoor">Indoor</span>
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
                <p class="text-gray-500 mt-2">Try adjusting your filters</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { courtService } from '@/services/courtService'

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const courts = ref([])
const categories = ref([])
const searchQuery = ref('')
const filterCity = ref('')
const filterCategory = ref('')
const filterIndoor = ref(false)
const maxPrice = ref(null)

const uniqueCities = computed(() => {
    const cities = [...new Set(courts.value.map(c => c.city))].filter(Boolean)
    return cities.sort()
})

const filteredCourts = computed(() => {
    return courts.value.filter(court => {
        const matchesSearch = !searchQuery.value ||
            court.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            court.city?.toLowerCase().includes(searchQuery.value.toLowerCase())

        const matchesCity = !filterCity.value || court.city === filterCity.value
        const matchesCategory = !filterCategory.value || court.category === filterCategory.value
        const matchesIndoor = !filterIndoor.value || court.is_indoor
        const matchesPrice = !maxPrice.value || court.base_hourly_rate <= maxPrice.value

        return matchesSearch && matchesCity && matchesCategory && matchesIndoor && matchesPrice
    })
})

const loadCourts = async () => {
    loading.value = true
    error.value = null
    try {
        const response = await courtService.getCourts()
        courts.value = response.results || response
    } catch (err) {
        console.error('Failed to load courts:', err)
        error.value = 'Failed to load courts. Please try again.'
    } finally {
        loading.value = false
    }
}

const loadCategories = async () => {
    try {
        categories.value = await courtService.getCategories()
    } catch (err) {
        console.error('Failed to load categories:', err)
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
    loadCategories()
})
</script>