<!-- views/court/CourtsView.vue -->
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
        <div class="search-section">
          <label for="search-input" class="input-label">Search Courts</label>
          <input id="search-input" v-model="searchQuery" type="search" placeholder="Court name, location, sport..."
            class="search-input" autocomplete="off" />
        </div>

        <div class="filters-grid">
          

          <div class="filter-group">
            <label for="city-filter" class="input-label">Location</label>
            <select id="city-filter" v-model="filterCity" class="filter-select">
              <option value="">All Locations</option>
              <option v-for="city in uniqueCities" :key="city" :value="city">
                {{ city }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label for="price-range" class="input-label">
              Max Price: <span class="price-value">Rs {{ maxPrice || 'Any' }}</span>
            </label>
            <input id="price-range" v-model.number="maxPrice" type="range" min="0" :max="maxPossiblePrice" step="100"
              class="price-slider" aria-valuemin="0" :aria-valuemax="maxPossiblePrice" :aria-valuenow="maxPrice"
              :aria-valuetext="`Rs ${maxPrice || 'Any'}`" />
          </div>

          <div class="filter-group">
            <label for="sort-select" class="input-label">Sort By</label>
            <select id="sort-select" v-model="sortBy" class="filter-select">
              <option value="rating">Highest Rated</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="name">Name</option>
            </select>
          </div>

          <div class="filter-group results-count">
            <span class="count-number">{{ sortedCourts.length }}</span>
            <span class="count-text">courts found</span>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-container">
        <div class="spinner" aria-label="Loading courts"></div>
        <p class="loading-text">Loading courts...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-container">
        <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="error-message">{{ error }}</p>
        <button @click="loadCourts" class="retry-button">
          Try Again
        </button>
      </div>

      <!-- Courts Grid using CourtCard component -->
      <div v-else-if="sortedCourts.length > 0" class="courts-grid">
        <CourtCard v-for="court in sortedCourts" :key="court.id" :court="court" @toggle-favorite="toggleFavorite"
          class="court-card-wrapper" />
      </div>

      <!-- Empty State -->
      <div v-else class="empty-container">
        <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <p class="empty-title">No courts found</p>
        <p class="empty-subtitle">Try changing or removing some filters</p>
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
import CourtCard from '@/components/Card.vue'          // ← Using the reusable card component
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

const maxPossiblePrice = computed(() => {
  if (!courts.value.length) return 5000
  return Math.max(...courts.value.map(c => parseFloat(c.base_hourly_rate) || 0)) + 500
})

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
      favorites.value.push(courtId) // rollback
    }
  } else {
    favorites.value.push(courtId)
    try {
      await courtService.addToFavorites(courtId)
    } catch (err) {
      console.error('Failed to add to favorites:', err)
      const idx = favorites.value.indexOf(courtId)
      if (idx > -1) favorites.value.splice(idx, 1) // rollback
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

  // Apply query params if present
  if (route.query.search) searchQuery.value = route.query.search
  if (route.query.city) filterCity.value = route.query.city
  if (route.query.category) filterCategory.value = route.query.category
  if (route.query.maxPrice) maxPrice.value = parseInt(route.query.maxPrice)
  if (route.query.sortBy) sortBy.value = route.query.sortBy
})

watch([searchQuery, filterCity, filterCategory, maxPrice, sortBy], () => {
  // Optional: debounce heavy operations if needed
})
</script>

<style scoped>
/* Keep your existing styles */
/* You might want to remove or adjust the old .court-card styles */
/* since the component now handles most of it */

.courts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.court-card-wrapper {
  height: 100%;
}

/* Optional: make sure the wrapper doesn't interfere with component hover effects */
.court-card-wrapper:hover {
  transform: none;
  /* Let the component handle hover */
}


:root {
  --primary: #10b981;
  --primary-dark: #059669;
  --primary-light: #d1fae5;
  --primary-glow: rgba(16, 185, 129, 0.25);
  --text: #111827;
  --text-secondary: #4b5563;
  --text-muted: #6b7280;
  --bg-card: #ffffff;
  --border: #e5e7eb;
  --danger: #ef4444;
}

.courts-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  padding: 2.5rem 1rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-size: clamp(2rem, 5vw, 3.2rem);
  font-weight: 800;
  color: var(--primary-dark);
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
}

/* Focus management - only show on keyboard navigation */
:focus-visible {
  outline: none;
}

button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
article[role="button"]:focus-visible {
  box-shadow: 0 0 0 3px white, 0 0 0 6px var(--primary-glow);
  border-radius: 12px;
  position: relative;
  z-index: 1;
}

/* ── Filters ── */
.filters-card {
  background: var(--bg-card);
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--border);
  margin: 2rem 0;
}

.search-input,
.filter-select {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid var(--border);
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.search-input:focus,
.filter-select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px var(--primary-glow);
  outline: none;
}

/* Better range slider */
.price-slider {
  width: 100%;
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(to right, var(--primary-light) 0%, var(--primary) 100%);
  outline: none;
  -webkit-appearance: none;
}

.price-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 28px;
  height: 28px;
  background: var(--primary);
  border: 4px solid white;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

.price-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

/* ── Court Card ── */
.court-card {
  background: var(--bg-card);
  border-radius: 1rem;
  overflow: hidden;
  border: 1px solid var(--border);
  transition: all 0.25s ease;
  cursor: pointer;
}

.court-card:hover,
.court-card:focus-visible {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px -10px rgba(16, 185, 129, 0.25);
  border-color: var(--primary);
}

.court-image {
  transition: transform 0.4s ease;
}

.court-card:hover .court-image {
  transform: scale(1.08);
}

.favorite-button {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(6px);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.favorite-button:hover {
  transform: scale(1.15);
  background: white;
}

.book-button {
  width: 100%;
  padding: 1rem;
  background: var(--primary);
  color: white;
  font-weight: 600;
  border-radius: 0.75rem;
  font-size: 1.05rem;
  transition: all 0.2s ease;
  min-height: 52px;
  /* better touch target */
}

.book-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

/* ── Text contrast improvements ── */
.court-description,
.court-location span,
.amenities-label,
.empty-subtitle,
.reviews-count,
.count-text {
  color: var(--text-muted);
}

/* ── Mobile adjustments ── */
@media (max-width: 640px) {
  .filters-grid {
    flex-direction: column;
  }

  .court-card {
    min-height: 420px;
    /* prevent layout shift */
  }
}

/* Updated color scheme to green/sporty theme */
:root {
  --primary-green: #10B981;
  --dark-green: #059669;
  --light-green: #D1FAE5;
  --accent-lime: #84CC16;
  --red-accent: #EF4444;
  --charcoal-text: #1F2937;
  --muted-text: #9CA3AF;
}

/* Main Container */
.courts-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
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
  color: var(--dark-green);
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
  border: 2px solid var(--light-green);
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
  border-color: var(--primary-green);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
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
  border-color: var(--primary-green);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.price-value {
  font-weight: 700;
  color: var(--primary-green);
}

.price-slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(to right, #a7f3d0 0%, var(--primary-green) 100%);
  outline: none;
  cursor: pointer;
  appearance: none;
}

.price-slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-green);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  transition: all 0.2s ease;
}

.price-slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.price-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-green);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  transition: all 0.2s ease;
}

.price-slider::-moz-range-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
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
  color: var(--primary-green);
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
  border-top-color: var(--primary-green);
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
  color: var(--red-accent);
  margin: 0 auto 16px;
}

.error-message {
  font-size: 20px;
  color: var(--muted-text);
  margin: 0 0 24px 0;
}

.retry-button {
  padding: 14px 32px;
  background: var(--primary-green);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-button:hover {
  background: var(--dark-green);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
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
  box-shadow: 0 12px 24px rgba(16, 185, 129, 0.2), 0 4px 8px rgba(0, 0, 0, 0.08);
  border-color: var(--primary-green);
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
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  width: 80px;
  height: 80px;
  color: var(--dark-green);
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
  color: var(--red-accent);
}

.available-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 6px 14px;
  background: var(--primary-green);
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
  color: var(--primary-green);
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
  color: var(--primary-green);
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
  background: var(--light-green);
  color: var(--dark-green);
}

.amenity-success {
  background: var(--accent-lime);
  color: white;
}

/* Book Button */
.book-button {
  width: 100%;
  padding: 14px;
  background: var(--primary-green);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.book-button:hover {
  background: var(--dark-green);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
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
  background: var(--primary-green);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-filters-button:hover {
  background: var(--dark-green);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
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
