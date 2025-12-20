<template>
  <div class="courts-view">
    <div class="container">
      <!-- Header -->
      <div class="header">
        <h1 class="page-title">All Available Courts</h1>
        <p class="page-subtitle">Find and book the perfect court for your game</p>
      </div>

      <!-- Search and Filters Card -->
      <div class="filters-card">
        <!-- Search -->
        <div class="search-section">
          <label class="input-label">Search Courts</label>
          <input v-model="searchQuery" type="text" placeholder="Search by court name, location, or sport type..."
            class="search-input" />
        </div>

        <div class="filters-grid">
          <!-- Sport Filter -->
          <div class="filter-group">
            <label class="input-label">Sport Type</label>
            <select v-model="filterCategory" class="filter-select">
              <option value="">All Sports</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <!-- Location Filter -->
          <div class="filter-group">
            <label class="input-label">Location</label>
            <select v-model="filterCity" class="filter-select">
              <option value="">All Locations</option>
              <option v-for="city in uniqueCities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>

          <!-- Price Range -->
          <div class="filter-group">
            <label class="input-label">Max Price: <span class="price-value">Rs {{ maxPrice || 'Any' }}</span></label>
            <input v-model.number="maxPrice" type="range" min="0" max="5000" step="100" class="price-slider" />
          </div>

          <!-- Sort By -->
          <div class="filter-group">
            <label class="input-label">Sort By</label>
            <select v-model="sortBy" class="filter-select">
              <option value="rating">Highest Rated</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="name">Name</option>
            </select>
          </div>

          <!-- Results Count -->
          <div class="filter-group results-count">
            <span class="count-number">{{ sortedCourts.length }}</span>
            <span class="count-text">courts found</span>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-text">Loading courts...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-container">
        <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="error-message">{{ error }}</p>
        <button @click="loadCourts" class="retry-button">
          Try Again
        </button>
      </div>

      <!-- Courts Grid -->
      <div v-else-if="sortedCourts.length > 0" class="courts-grid">
        <div v-for="court in sortedCourts" :key="court.id" class="court-card" @click="viewCourtDetail(court.id)">
          <!-- Court Image -->
          <div class="court-image-container">
            <img v-if="court.primary_image" :src="court.primary_image" :alt="court.name" class="court-image" />
            <div v-else class="court-image-placeholder">
              <svg class="placeholder-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>

            <!-- Favorite Button -->
            <button @click.stop="toggleFavorite(court.id)" class="favorite-button">
              <svg :class="['heart-icon', favorites.includes(court.id) ? 'favorited' : '']" fill="currentColor"
                viewBox="0 0 24 24">
                <path
                  d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
              </svg>
            </button>

            <!-- Available Badge -->
            <div class="available-badge">Available</div>
          </div>

          <!-- Court Info -->
          <div class="court-info">
            <h3 class="court-name">{{ court.name }}</h3>
            <p class="court-description">
              {{ court.description || 'Professional sports facility with premium amenities' }}
            </p>

            <!-- Location -->
            <div class="court-location">
              <svg class="location-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>{{ court.city }}</span>
            </div>

            <!-- Rating and Price -->
            <div class="court-meta">
              <div class="rating-container">
                <div class="rating-stars">
                  <svg class="star-icon" viewBox="0 0 24 24">
                    <path
                      d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                  </svg>
                  <span class="rating-value">{{ court.average_rating || '4.5' }}</span>
                </div>
                <span class="reviews-count">({{ court.total_reviews || 0 }})</span>
              </div>
              <span class="court-price">Rs {{ court.base_hourly_rate }}/hr</span>
            </div>

            <!-- Amenities -->
            <div class="amenities-section">
              <p class="amenities-label">Amenities:</p>
              <div class="amenities-tags">
                <span class="amenity-tag amenity-primary">
                  {{ court.is_indoor ? 'Indoor' : 'Outdoor' }}
                </span>
                <span v-if="court.is_verified" class="amenity-tag amenity-success">
                  Verified
                </span>
                <span class="amenity-tag amenity-primary">
                  {{ court.category_name || court.court_type }}
                </span>
              </div>
            </div>

            <!-- Book Button -->
            <button @click.stop="viewCourtDetail(court.id)" class="book-button">
              Book Now
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-container">
        <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <p class="empty-title">No courts found matching your criteria</p>
        <p class="empty-subtitle">Try adjusting your filters to see more results</p>
        <button @click="clearFilters" class="clear-filters-button">
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

  if (filterCity.value) {
    filtered = filtered.filter(court => court.city === filterCity.value)
  }

  if (filterCategory.value) {
    filtered = filtered.filter(court => court.category === parseInt(filterCategory.value))
  }

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
    try {
      await courtService.removeFromFavorites(courtId)
    } catch (err) {
      console.error('Failed to remove from favorites:', err)
      favorites.value.push(courtId)
    }
  } else {
    favorites.value.push(courtId)
    try {
      await courtService.addToFavorites(courtId)
    } catch (err) {
      console.error('Failed to add to favorites:', err)
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

onMounted(() => {
  loadCourts()
  loadCategories()
  loadFavorites()

  if (route.query.search) searchQuery.value = route.query.search
  if (route.query.city) filterCity.value = route.query.city
  if (route.query.category) filterCategory.value = route.query.category
  if (route.query.maxPrice) maxPrice.value = parseInt(route.query.maxPrice)
  if (route.query.sortBy) sortBy.value = route.query.sortBy
})

let searchTimeout = null
watch(searchQuery, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      updateURLQuery()
    }, 500)
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

  const currentQuery = JSON.stringify(route.query)
  const newQuery = JSON.stringify(query)
  if (currentQuery !== newQuery) {
    router.replace({ query })
  }
}
</script>

<style scoped>
/* Color Variables */
:root {
  --primary-blue: #0056B3;
  --red-cta: #EF4444;
  --purple-accent: #7C3AED;
  --success-green: #10B981;
  --warning-orange: #F59E0B;
  --charcoal-text: #1F2937;
  --muted-text: #9CA3AF;
  --orange: #FF6B35;
}

/* Main Container */
.courts-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 40px 0;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Header */
.header {
  margin-bottom: 32px;
  text-align: center;
}

.page-title {
  font-size: 40px;
  font-weight: 800;
  color: var(--charcoal-text);
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.page-subtitle {
  font-size: 18px;
  color: var(--muted-text);
  margin: 0;
}

/* Filters Card */
.filters-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 32px;
  border: 1px solid #e5e7eb;
}

.search-section {
  margin-bottom: 24px;
}

.input-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--charcoal-text);
  margin-bottom: 8px;
}

.search-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  color: var(--charcoal-text);
  background: white;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

.search-input::placeholder {
  color: var(--muted-text);
}

.filters-grid {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-group {
  flex: 1;
  min-width: 180px;
}

.filter-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  color: var(--charcoal-text);
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

.price-value {
  font-weight: 700;
  color: var(--primary-blue);
}

.price-slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(to right, #bfdbfe 0%, var(--primary-blue) 100%);
  outline: none;
  cursor: pointer;
  appearance: none;
}

.price-slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-blue);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 86, 179, 0.3);
  transition: all 0.2s ease;
}

.price-slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.4);
}

.price-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-blue);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 86, 179, 0.3);
  transition: all 0.2s ease;
}

.price-slider::-moz-range-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.4);
}

.results-count {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding-bottom: 4px;
}

.count-number {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-blue);
  line-height: 1;
}

.count-text {
  font-size: 13px;
  color: var(--muted-text);
  margin-top: 2px;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top-color: var(--primary-blue);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  margin-top: 16px;
  font-size: 16px;
  color: var(--muted-text);
  font-weight: 500;
}

/* Error State */
.error-container {
  text-align: center;
  padding: 80px 20px;
}

.error-icon {
  width: 64px;
  height: 64px;
  color: var(--red-cta);
  margin: 0 auto 16px;
}

.error-message {
  font-size: 20px;
  color: var(--muted-text);
  margin: 0 0 24px 0;
}

.retry-button {
  padding: 14px 32px;
  background: var(--primary-blue);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-button:hover {
  background: #003d82;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
}

/* Courts Grid */
.courts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.court-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s ease;
}

.court-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1), 0 4px 8px rgba(0, 0, 0, 0.08);
}

/* Court Image */
.court-image-container {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.court-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.court-card:hover .court-image {
  transform: scale(1.05);
}

.court-image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #dbeafe 0%, #e9d5ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  width: 80px;
  height: 80px;
  color: var(--muted-text);
  opacity: 0.5;
}

.favorite-button {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 40px;
  height: 40px;
  background: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
  z-index: 2;
}

.favorite-button:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.heart-icon {
  width: 20px;
  height: 20px;
  color: var(--muted-text);
  transition: all 0.2s ease;
}

.heart-icon.favorited {
  color: var(--red-cta);
}

.available-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 6px 14px;
  background: var(--success-green);
  color: white;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

/* Court Info */
.court-info {
  padding: 20px;
}

.court-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--charcoal-text);
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.court-description {
  font-size: 14px;
  color: var(--muted-text);
  margin: 0 0 16px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.court-location {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--muted-text);
  margin-bottom: 16px;
}

.location-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* Court Meta */
.court-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.rating-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-stars {
  display: flex;
  align-items: center;
  gap: 4px;
}

.star-icon {
  width: 16px;
  height: 16px;
  fill: #FBBF24;
  color: #FBBF24;
}

.rating-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--charcoal-text);
}

.reviews-count {
  font-size: 12px;
  color: var(--muted-text);
}

.court-price {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-blue);
}

/* Amenities */
.amenities-section {
  margin-bottom: 16px;
}

.amenities-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--muted-text);
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.amenities-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.amenity-tag {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.amenity-primary {
  background: #dbeafe;
  color: var(--primary-blue);
}

.amenity-success {
  background: #d1fae5;
  color: var(--success-green);
}

/* Book Button */
.book-button {
  width: 100%;
  padding: 14px;
  background: var(--primary-blue);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.book-button:hover {
  background: #e55a2b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

/* Empty State */
.empty-container {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  width: 96px;
  height: 96px;
  color: var(--muted-text);
  margin: 0 auto 16px;
  opacity: 0.5;
}

.empty-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--charcoal-text);
  margin: 0 0 8px 0;
}

.empty-subtitle {
  font-size: 16px;
  color: var(--muted-text);
  margin: 0 0 24px 0;
}

.clear-filters-button {
  padding: 14px 32px;
  background: var(--primary-blue);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-filters-button:hover {
  background: #003d82;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-title {
    font-size: 32px;
  }

  .page-subtitle {
    font-size: 16px;
  }

  .filters-card {
    padding: 20px;
  }

  .filters-grid {
    flex-direction: column;
  }

  .filter-group {
    min-width: 100%;
  }

  .courts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 16px;
  }

  .page-title {
    font-size: 28px;
  }
}
</style>
