<!-- views/HomeView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">

    <!-- ==================== HERO ==================== -->
    <section
      class="relative overflow-hidden bg-gradient-to-br from-green-600 via-emerald-700 to-teal-800 py-16 lg:py-28">
      <div class="absolute inset-0 bg-grid-white/5 opacity-10"></div>
      <div class="absolute -top-24 -right-24 w-96 h-96 bg-teal-400 rounded-full blur-3xl opacity-20"></div>
      <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-emerald-400 rounded-full blur-3xl opacity-20"></div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="text-white">
            <span
              class="inline-flex items-center gap-2 px-4 py-1.5 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full text-sm font-medium mb-6">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              Multi-Sport Booking Platform
            </span>

            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight mb-6">
              Book Your Perfect
              <span class="block text-emerald-200">Sports Court</span>
            </h1>

            <p class="text-lg sm:text-xl text-emerald-100/90 mb-8 max-w-xl">
              Reserve premium futsal, basketball, tennis, badminton & multi-sport courts instantly.
            </p>

            <div class="flex flex-wrap gap-4">
              <button @click="scrollToSearch"
                class="group inline-flex items-center gap-2 bg-white hover:bg-emerald-50 text-emerald-700 px-8 py-4 rounded-xl font-semibold transition-all shadow-lg hover:shadow-xl hover:scale-[1.02]">
                Find a Court
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </button>
            </div>
          </div>

          <div class="hidden lg:block">
            <div class="relative">
              <div class="absolute inset-0 bg-teal-500/10 rounded-3xl blur-xl"></div>
              <div class="relative bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 shadow-2xl">
                <div class="grid grid-cols-3 gap-6">
                  <div class="bg-white/10 rounded-xl p-5 text-center">
                    <p class="text-3xl font-bold text-white">500+</p>
                    <p class="text-sm text-emerald-200 mt-1">Courts</p>
                  </div>
                  <div class="bg-white/10 rounded-xl p-5 text-center">
                    <p class="text-3xl font-bold text-white">25K+</p>
                    <p class="text-sm text-emerald-200 mt-1">Players</p>
                  </div>
                  <div class="bg-white/10 rounded-xl p-5 text-center">
                    <p class="text-3xl font-bold text-white">50+</p>
                    <p class="text-sm text-emerald-200 mt-1">Cities</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== SEARCH ==================== -->
    <section class="relative -mt-16 pb-20 px-4 sm:px-6 lg:px-8">
      <div ref="searchSection"
        class="max-w-6xl mx-auto bg-white rounded-2xl shadow-2xl border border-emerald-100 overflow-hidden">
        <div class="bg-gradient-to-r from-emerald-50 to-teal-50 px-8 py-6 border-b border-emerald-100">
          <h2 class="text-2xl font-bold text-gray-900 mb-1">Find Your Perfect Court</h2>
          <p class="text-gray-600">Sport • Location • Date</p>
        </div>

        <div class="p-8">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="space-y-2">
              <label class="flex items-center gap-2 text-sm font-semibold text-gray-700">
                <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Sport
              </label>
              <select v-model="searchFilters.sport"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent">
                <option value="">All Sports</option>
                <option value="Basketball">🏀 Basketball</option>
                <option value="Football">⚽ Football</option>
                <option value="Futsal">🥅 Futsal</option>
                <option value="Tennis">🎾 Tennis</option>
                <option value="Badminton">🏸 Badminton</option>
              </select>
            </div>

            <div class="space-y-2">
              <label class="flex items-center gap-2 text-sm font-semibold text-gray-700">
                <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                </svg>
                Location
              </label>
              <input v-model="searchFilters.location" type="text" placeholder="City or area"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent" />
            </div>

            <div class="space-y-2">
              <label class="flex items-center gap-2 text-sm font-semibold text-gray-700">
                <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Date
              </label>
              <input v-model="searchFilters.date" type="date" :min="minDate"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent" />
            </div>

            <div class="flex items-end">
              <button @click="handleSearch"
                class="w-full py-3.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl font-semibold shadow-md hover:shadow-lg flex items-center justify-center gap-2 transition-all">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== HOW IT WORKS ==================== -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <span
            class="inline-block px-4 py-1.5 bg-emerald-100 text-emerald-700 rounded-full text-sm font-semibold mb-4">
            SIMPLE PROCESS
          </span>
          <h2 class="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">How It Works</h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">Book your court in just 4 easy steps</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div v-for="(step, index) in steps" :key="index" class="text-center group">
            <div class="relative mb-6 inline-block">
              <div
                class="w-20 h-20 bg-gradient-to-br from-emerald-500 to-teal-600 text-white rounded-2xl flex items-center justify-center text-3xl font-bold shadow-lg group-hover:scale-110 transition-transform">
                {{ index + 1 }}
              </div>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{{ step.title }}</h3>
            <p class="text-gray-600">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== FEATURED COURTS ==================== -->
    <section class="py-20 bg-gradient-to-br from-green-50 to-emerald-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-12 gap-6">
          <div>
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-2">Featured Courts</h2>
            <p class="text-lg text-gray-600">Top-rated venues ready for your next game</p>
          </div>
          <router-link to="/courts"
            class="inline-flex items-center gap-2 text-emerald-600 hover:text-emerald-700 font-semibold group">
            View All Courts
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor"
              viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>

        <div v-if="loading" class="flex justify-center py-20">
          <div class="w-14 h-14 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
        </div>

        <div v-else-if="featuredCourts.length === 0" class="text-center py-12 text-gray-500">
          No featured courts available at the moment
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <CourtCard v-for="court in featuredCourts" :key="court.id" :court="court" />
        </div>
      </div>
    </section>

    <!-- ==================== STATS BANNER ==================== -->
    <section
      class="py-20 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-700 text-white relative overflow-hidden">
      <div class="absolute inset-0 bg-grid-white/5 opacity-10"></div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
          <div class="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
            <p class="text-5xl font-bold mb-2">500+</p>
            <p class="text-lg text-emerald-100">Active Courts</p>
          </div>
          <div class="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
            <p class="text-5xl font-bold mb-2">25K+</p>
            <p class="text-lg text-emerald-100">Happy Players</p>
          </div>
          <div class="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
            <p class="text-5xl font-bold mb-2">100K+</p>
            <p class="text-lg text-emerald-100">Bookings</p>
          </div>
          <div class="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
            <p class="text-5xl font-bold mb-2">50+</p>
            <p class="text-lg text-emerald-100">Cities</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== TESTIMONIALS ==================== -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <span
            class="inline-block px-4 py-1.5 bg-emerald-100 text-emerald-700 rounded-full text-sm font-semibold mb-4">
            TESTIMONIALS
          </span>
          <h2 class="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">What Players Say</h2>
          <p class="text-xl text-gray-600">Loved by thousands of athletes</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="(testimonial, i) in testimonials" :key="i"
            class="bg-gradient-to-br from-emerald-50 to-teal-50 p-8 rounded-2xl border border-emerald-100 hover:shadow-xl transition-all">
            <div class="flex gap-1 mb-6">
              <svg v-for="n in 5" :key="n" class="w-6 h-6 text-amber-400 fill-current" viewBox="0 0 24 24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
            <p class="text-gray-700 italic text-lg leading-relaxed mb-8">“{{ testimonial.text }}”</p>
            <div class="flex items-center gap-4">
              <div
                class="w-14 h-14 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                {{ testimonial.initials }}
              </div>
              <div>
                <p class="font-bold text-gray-900">{{ testimonial.name }}</p>
                <p class="text-sm text-gray-600">{{ testimonial.role }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import CourtCard from '@/components/Card.vue'          // ← Import the reusable card component
import { courtService } from '@/services/courtService'

const router = useRouter()

const loading = ref(false)
const featuredCourts = ref([])

const searchFilters = ref({
  sport: '',
  location: '',
  date: ''
})

const searchSection = ref(null)

const minDate = computed(() => new Date().toISOString().split('T')[0])

const steps = [
  { title: 'Search & Explore', description: 'Find courts near you with all details & reviews' },
  { title: 'Choose Date & Time', description: 'Pick the perfect slot that fits your schedule' },
  { title: 'Book Securely', description: 'Instant confirmation with safe payment' },
  { title: 'Play & Enjoy', description: 'Just show up and have an amazing game!' }
]

const testimonials = [
  {
    text: "BookACourt completely changed how I organize my weekend games. Super easy and reliable!",
    name: "Alex Rivera",
    role: "Futsal Captain",
    initials: "AR"
  },
  {
    text: "Best platform for finding quality basketball courts. Booking takes seconds, courts are always great.",
    name: "Maya Chen",
    role: "Basketball Player",
    initials: "MC"
  },
  {
    text: "Used it for our corporate tournament — smooth process from start to finish. Highly recommended!",
    name: "David Kim",
    role: "Team Organizer",
    initials: "DK"
  }
]

const handleSearch = () => {
  router.push({
    path: '/courts',
    query: { ...searchFilters.value }
  })
}

const scrollToSearch = () => {
  searchSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const loadFeaturedCourts = async () => {
  loading.value = true
  try {
    const response = await courtService.getCourts({ page_size: 8 })
    featuredCourts.value = response.results?.slice(0, 4) || response.slice(0, 4) || []
  } catch (error) {
    console.error('Failed to load featured courts:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadFeaturedCourts()
})
</script>