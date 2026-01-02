<!-- components/CourtCard.vue -->
<template>
  <div
    class="group bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-xl transition-all border border-gray-200 cursor-pointer h-full flex flex-col"
    @click="goToCourtDetail"
  >
    <!-- Image + Category Tag -->
    <div class="relative h-48 overflow-hidden flex-shrink-0">
      <img
        v-if="court.primary_image"
        :src="court.primary_image"
        :alt="court.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <div
        v-else
        class="w-full h-full bg-gradient-to-br from-emerald-100 to-teal-100 flex items-center justify-center"
      >
        <svg
          class="w-20 h-20 text-emerald-200"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
          />
        </svg>
      </div>

      <span
        class="absolute top-4 left-4 px-3 py-1 bg-white/90 backdrop-blur-sm text-emerald-700 text-xs font-bold rounded-full shadow"
      >
        {{ court.category_name || 'Multi-sport' }}
      </span>
    </div>

    <!-- Content -->
    <div class="p-5 flex flex-col flex-grow">
      <!-- Location -->
      <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
          />
        </svg>
        {{ court.city || 'City' }}
      </div>

      <!-- Name -->
      <h3
        class="font-bold text-lg text-gray-900 mb-3 group-hover:text-emerald-700 transition-colors line-clamp-2"
      >
        {{ court.name }}
      </h3>

      <!-- Rating + Status -->
      <div class="flex items-center justify-between mb-4 mt-auto">
        <div class="flex items-center gap-1">
          <svg class="w-5 h-5 text-amber-400 fill-current" viewBox="0 0 24 24">
            <path
              d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
            />
          </svg>
          <span class="font-bold">{{ court.average_rating || '4.8' }}</span>
        </div>

        <span class="text-sm font-semibold text-emerald-600 flex items-center gap-1.5">
          <span class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
          Available
        </span>
      </div>

      <!-- Price + Button -->
      <div class="flex items-center justify-between">
        <div>
          <p class="text-xs text-gray-500">From</p>
          <p class="text-xl font-bold text-emerald-700">
            Nrs. {{ court.base_hourly_rate || '–' }}
            <span class="text-sm font-normal text-gray-500">/hr</span>
          </p>
        </div>

        <button
          class="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium transition-colors"
        >
          Book Now
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  court: {
    type: Object,
    required: true
  }
})

const goToCourtDetail = () => {
  router.push(`/courts/${props.court.id}`)
}
</script>