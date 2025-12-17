<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">All Available Courts</h1>
      </div>

      <!-- Search and Filters Card -->
      <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200 mb-8">
        <!-- Search -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-900 mb-2">Search Courts</label>
          <input v-model="searchQuery" type="text" placeholder="Search by court name..."
            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-[#0056B3] focus:border-transparent" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <!-- Sport Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-900 mb-2">Sport Type</label>
            <select v-model="filterCategory"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-lg bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-[#0056B3] focus:border-transparent">
              <option value="">All Sports</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <!-- Location Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-900 mb-2">Location</label>
            <select v-model="filterCity"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-lg bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-[#0056B3] focus:border-transparent">
              <option value="">All Locations</option>
              <option v-for="city in uniqueCities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>

          <!-- Price Range -->
          <div>
            <label class="block text-sm font-medium text-gray-900 mb-2">Max Price: Rs {{ maxPrice || 'Any' }}</label>
            <input v-model.number="maxPrice" type="range" min="0" max="5000" step="100"
              class="w-full h-2 bg-blue-200 rounded-lg appearance-none cursor-pointer slider-thumb" />
          </div>

          <!-- Sort By -->
          <div>
            <label class="block text-sm font-medium text-gray-900 mb-2">Sort By</label>
            <select v-model="sortBy"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-lg bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-[#0056B3] focus:border-transparent">
              <option value="rating">Highest Rated</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
            </select>
          </div>

          <!-- Results Count -->
          <div class="flex items-end">
            <div class="text-sm text-gray-600">
              <span class="font-semibold text-gray-900">{{ sortedCourts.length }}</span> courts found
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-gray-200 border-t-[#0056B3]"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-20">
        <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-xl text-gray-600 mb-4">{{ error }}</p>
        <button @click="loadCourts" class="px-6 py-3 bg-[#0056B3] text-white rounded-lg hover:bg-[#003D82] transition">
          Try Again
        </button>
      </div>

      <!-- Courts Grid -->
      <div v-else-if="sortedCourts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="court in sortedCourts" :key="court.id"
          class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-shadow border border-gray-200 cursor-pointer"
          @click="viewCourtDetail(court.id)">
          <!-- Court Image -->
          <div class="relative h-48">
            <img v-if="court.primary_image" :src="court.primary_image" :alt="court.name"
              class="w-full h-full object-cover" />
            <div v-else
              class="w-full h-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
              <svg class="w-20 h-20 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>

            <!-- Favorite Button -->
            <button @click.stop="toggleFavorite(court.id)"
              class="absolute top-3 right-3 p-2 bg-white rounded-full shadow-md hover:bg-gray-100 transition">
              <svg :class="['w-5 h-5', favorites.includes(court.id) ? 'fill-red-500 text-red-500' : 'text-gray-600']"
                fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
              </svg>
            </button>

            <!-- Available Badge -->
            <div class="absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-semibold bg-[#10B981] text-white">
              Available
            </div>
          </div>

          <!-- Court Info -->
          <div class="p-4">
            <h3 class="text-lg font-bold text-gray-900 mb-2">{{ court.name }}</h3>
            <p class="text-sm text-gray-600 mb-3 line-clamp-2">
              {{ court.description || 'Professional sports facility with premium amenities' }}
            </p>

            <!-- Location -->
            <div class="flex items-center gap-2 text-sm text-gray-600 mb-3">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {{ court.city }}
            </div>

            <!-- Rating and Price -->
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <div class="flex items-center gap-1">
                  <svg class="w-4 h-4 fill-yellow-400 text-yellow-400" viewBox="0 0 24 24">
                    <path
                      d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                  </svg>
                  <span class="text-sm font-semibold text-gray-900">{{ court.average_rating || '4.5' }}</span>
                </div>
                <span class="text-xs text-gray-500">({{ court.total_reviews || 0 }})</span>
              </div>
              <span class="text-lg font-bold text-[#0056B3]">Rs {{ court.base_hourly_rate }}/hr</span>
            </div>

            <!-- Amenities -->
            <div class="mb-4">
              <p class="text-xs font-medium text-gray-600 mb-2">Amenities:</p>
              <div class="flex flex-wrap gap-2">
                <span class="text-xs bg-[#E3F2FD] text-[#0056B3] px-2 py-1 rounded">
                  {{ court.is_indoor ? 'Indoor' : 'Outdoor' }}
                </span>
                <span v-if="court.is_verified" class="text-xs bg-[#D1FAE5] text-[#10B981] px-2 py-1 rounded">
                  Verified
                </span>
                <span class="text-xs bg-[#E3F2FD] text-[#0056B3] px-2 py-1 rounded">
                  {{ court.category_name || court.court_type }}
                </span>
              </div>
            </div>

            <!-- Book Button -->
            <button @click.stop="viewCourtDetail(court.id)"
              class="w-full py-2.5 bg-[#FF6B35] text-white rounded-lg font-semibold hover:bg-[#E55A2B] transition text-center">
              Book Now
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-20">
        <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <p class="text-xl text-gray-600 mb-2">No courts found matching your criteria</p>
        <p class="text-gray-500 mb-4">Try adjusting your filters</p>
        <button @click="clearFilters"
          class="px-6 py-3 bg-[#0056B3] text-white rounded-lg hover:bg-[#003D82] transition">
          Clear All Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courtService } from '@/services/courtService'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const error = ref(null)
const courts = ref([])
const categories = ref([])
const favorites = ref([])
const searchQuery = ref('')
const filterCity = ref('')
const filterCategory = ref('')
const maxPrice = ref(5000)
const sortBy = ref('rating')

const uniqueCities = computed(() => {
  const cities = [...new Set(courts.value.map(c => c.city))].filter(Boolean)
  return cities.sort()
})

const filteredCourts = computed(() => {
  let filtered = [...courts.value]

  // Search filter - searches in name, city, description, and address
  if (searchQuery.value) {
    const search = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(court => {
      return (
        court.name?.toLowerCase().includes(search) ||
        court.city?.toLowerCase().includes(search) ||
        court.description?.toLowerCase().includes(search) ||
        court.address?.toLowerCase().includes(search) ||
        court.category_name?.toLowerCase().includes(search)
      )
    })
  }

  // City filter - exact match
  if (filterCity.value) {
    filtered = filtered.filter(court => court.city === filterCity.value)
  }

  // Category filter - matches category ID
  if (filterCategory.value) {
    filtered = filtered.filter(court => court.category === parseInt(filterCategory.value))
  }

  // Price filter - courts with hourly rate less than or equal to max price
  if (maxPrice.value) {
    filtered = filtered.filter(court => parseFloat(court.base_hourly_rate) <= maxPrice.value)
  }

  return filtered
})

const sortedCourts = computed(() => {
  const sorted = [...filteredCourts.value]

  switch (sortBy.value) {
    case 'price-low':
      return sorted.sort((a, b) => parseFloat(a.base_hourly_rate) - parseFloat(b.base_hourly_rate))
    case 'price-high':
      return sorted.sort((a, b) => parseFloat(b.base_hourly_rate) - parseFloat(a.base_hourly_rate))
    case 'rating':
      return sorted.sort((a, b) => {
        const ratingA = parseFloat(a.average_rating) || 0
        const ratingB = parseFloat(b.average_rating) || 0
        return ratingB - ratingA
      })
    case 'name':
      return sorted.sort((a, b) => a.name.localeCompare(b.name))
    default:
      return sorted
  }
})

const toggleFavorite = async (courtId) => {
  const index = favorites.value.indexOf(courtId)
  if (index > -1) {
    favorites.value.splice(index, 1)
    // Optionally: Call API to remove from favorites
    try {
      await courtService.removeFromFavorites(courtId)
    } catch (err) {
      console.error('Failed to remove from favorites:', err)
      // Re-add if API call fails
      favorites.value.push(courtId)
    }
  } else {
    favorites.value.push(courtId)
    // Optionally: Call API to add to favorites
    try {
      await courtService.addToFavorites(courtId)
    } catch (err) {
      console.error('Failed to add to favorites:', err)
      // Remove if API call fails
      const idx = favorites.value.indexOf(courtId)
      if (idx > -1) favorites.value.splice(idx, 1)
    }
  }
}

const loadFavorites = async () => {
  try {
    const response = await courtService.getFavoriteCourts()
    favorites.value = (response.results || response).map(court => court.id)
  } catch (err) {
    console.error('Failed to load favorites:', err)
  }
}

const clearFilters = () => {
  searchQuery.value = ''
  filterCity.value = ''
  filterCategory.value = ''
  maxPrice.value = 5000
  sortBy.value = 'rating'
  router.replace({ query: {} })
}

const loadCourts = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await courtService.getCourts()
    courts.value = response.results || response
    console.log('Loaded courts:', courts.value.length)
  } catch (err) {
    console.error('Failed to load courts:', err)
    error.value = 'Failed to load courts. Please try again.'
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await courtService.getCategories()
    categories.value = response.results || response
    console.log('Loaded categories:', categories.value)
  } catch (err) {
    console.error('Failed to load categories:', err)
  }
}

const viewCourtDetail = (courtId) => {
  router.push(`/courts/${courtId}`)
}

// Initialize filters from URL query params on mount
onMounted(() => {
  // Load data first
  loadCourts()
  loadCategories()
  loadFavorites()

  // Then initialize filters from URL
  if (route.query.search) searchQuery.value = route.query.search
  if (route.query.city) filterCity.value = route.query.city
  if (route.query.category) filterCategory.value = route.query.category
  if (route.query.maxPrice) maxPrice.value = parseInt(route.query.maxPrice)
  if (route.query.sortBy) sortBy.value = route.query.sortBy
})

// Update URL when filters change (debounced for search)
let searchTimeout = null
watch(searchQuery, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      updateURLQuery()
    }, 500) // 500ms debounce for search
  }
})

watch([filterCity, filterCategory, maxPrice, sortBy], () => {
  updateURLQuery()
}, { deep: true })

const updateURLQuery = () => {
  const query = {}
  if (searchQuery.value) query.search = searchQuery.value
  if (filterCity.value) query.city = filterCity.value
  if (filterCategory.value) query.category = filterCategory.value
  if (maxPrice.value && maxPrice.value < 5000) query.maxPrice = maxPrice.value.toString()
  if (sortBy.value && sortBy.value !== 'rating') query.sortBy = sortBy.value

  // Only update if query has changed
  const currentQuery = JSON.stringify(route.query)
  const newQuery = JSON.stringify(query)
  if (currentQuery !== newQuery) {
    router.replace({ query })
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom slider thumb styling */
.slider-thumb::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #0056B3;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-thumb::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #0056B3;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-thumb::-webkit-slider-runnable-track {
  height: 8px;
  border-radius: 4px;
}

.slider-thumb::-moz-range-track {
  height: 8px;
  border-radius: 4px;
}
</style>