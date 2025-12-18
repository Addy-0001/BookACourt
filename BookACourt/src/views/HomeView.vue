<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
    <!-- Hero Section with Modern Gradient -->
    <section class="relative overflow-hidden bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 py-20 lg:py-32">
      <!-- Decorative Elements -->
      <div
        class="absolute inset-0 bg-grid-white/5 [mask-image:linear-gradient(0deg,transparent,rgba(255,255,255,0.5))]">
      </div>
      <div class="absolute top-0 right-0 -translate-y-12 translate-x-12 blur-3xl opacity-30">
        <div class="w-96 h-96 bg-cyan-400 rounded-full"></div>
      </div>
      <div class="absolute bottom-0 left-0 translate-y-12 -translate-x-12 blur-3xl opacity-30">
        <div class="w-96 h-96 bg-purple-400 rounded-full"></div>
      </div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <!-- Left Content -->
          <div class="text-white">
            <span
              class="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm border border-white/20 text-white rounded-full text-sm font-medium mb-6">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              Your Multi-Sport Booking Platform
            </span>
            <h1 class="text-5xl lg:text-6xl xl:text-7xl font-bold mb-6 leading-tight">
              Book Your Perfect
              <span class="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-blue-200">
                Sports Court
              </span>
            </h1>
            <p class="text-xl text-blue-100 mb-8 leading-relaxed">
              Reserve premium futsal, basketball, and multi-sport courts instantly. Professional facilities, seamless
              bookings, unbeatable experience.
            </p>
            <div class="flex flex-wrap gap-4">
              <router-link to="/courts"
                class="group inline-flex items-center gap-2 bg-white hover:bg-blue-50 text-blue-600 px-8 py-4 rounded-xl font-semibold transition-all shadow-xl hover:shadow-2xl hover:scale-105">
                Browse Courts
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </router-link>
              <button
                class="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20 text-white px-8 py-4 rounded-xl font-semibold transition-all">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Watch Demo
              </button>
            </div>
          </div>

          <!-- Right Visual -->
          <div class="hidden lg:block">
            <div class="relative">
              <div class="absolute inset-0 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-3xl blur-2xl opacity-20">
              </div>
              <div class="relative bg-white/10 backdrop-blur-md border border-white/20 rounded-3xl p-8 shadow-2xl">
                <div
                  class="aspect-[4/3] bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl flex items-center justify-center overflow-hidden">
                  <svg class="w-32 h-32 text-white/20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <!-- Mini Stats -->
                <div class="grid grid-cols-3 gap-4 mt-6">
                  <div class="bg-white/5 backdrop-blur-sm rounded-xl p-3 text-center border border-white/10">
                    <p class="text-2xl font-bold text-white">500+</p>
                    <p class="text-xs text-blue-200">Courts</p>
                  </div>
                  <div class="bg-white/5 backdrop-blur-sm rounded-xl p-3 text-center border border-white/10">
                    <p class="text-2xl font-bold text-white">25K+</p>
                    <p class="text-xs text-blue-200">Users</p>
                  </div>
                  <div class="bg-white/5 backdrop-blur-sm rounded-xl p-3 text-center border border-white/10">
                    <p class="text-2xl font-bold text-white">50+</p>
                    <p class="text-xs text-blue-200">Cities</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Search Section with Elevated Card -->
    <section class="relative -mt-16 pb-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden">
          <div class="bg-gradient-to-r from-slate-50 to-blue-50 px-8 py-6 border-b border-slate-200">
            <h2 class="text-2xl font-bold text-slate-900 mb-1">Find Your Court</h2>
            <p class="text-slate-600">Filter by sport, location, and date to find available courts</p>
          </div>

          <div class="p-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Sport Type
                </label>
                <select v-model="searchFilters.sport"
                  class="w-full px-4 py-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white transition-shadow hover:shadow-md">
                  <option value="">All Sports</option>
                  <option value="Basketball">🏀 Basketball</option>
                  <option value="Football">⚽ Football</option>
                  <option value="Futsal">🥅 Futsal</option>
                  <option value="Tennis">🎾 Tennis</option>
                  <option value="Badminton">🏸 Badminton</option>
                </select>
              </div>

              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Location
                </label>
                <input v-model="searchFilters.location" type="text" placeholder="Enter city or area"
                  class="w-full px-4 py-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow hover:shadow-md" />
              </div>

              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Date
                </label>
                <input v-model="searchFilters.date" type="date" :min="minDate"
                  class="w-full px-4 py-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow hover:shadow-md" />
              </div>

              <div class="flex items-end">
                <button @click="handleSearch"
                  class="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2 group">
                  <svg class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Search
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <span class="inline-block px-4 py-2 bg-blue-100 text-blue-600 rounded-full text-sm font-semibold mb-4">
            SIMPLE PROCESS
          </span>
          <h2 class="text-4xl lg:text-5xl font-bold text-slate-900 mb-4">How It Works</h2>
          <p class="text-xl text-slate-600 max-w-2xl mx-auto">Book your perfect court in 4 simple steps</p>
        </div>

        <div class="relative">
          <!-- Connection Line -->
          <div
            class="hidden lg:block absolute top-16 left-1/4 right-1/4 h-0.5 bg-gradient-to-r from-blue-200 via-indigo-200 to-purple-200">
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 relative">
            <!-- Step 1 -->
            <div class="group text-center">
              <div class="relative mb-6 flex justify-center">
                <div
                  class="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-2xl flex items-center justify-center text-2xl font-bold shadow-lg group-hover:scale-110 transition-transform relative z-10">
                  1
                </div>
                <div
                  class="absolute inset-0 bg-blue-400 rounded-2xl blur-xl opacity-20 group-hover:opacity-30 transition-opacity">
                </div>
              </div>
              <div class="bg-slate-50 rounded-xl p-6 h-full hover:shadow-lg transition-shadow border border-slate-200">
                <h3 class="text-xl font-bold text-slate-900 mb-3">Search & Explore</h3>
                <p class="text-slate-600">Browse available courts in your area with detailed information and reviews</p>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="group text-center">
              <div class="relative mb-6 flex justify-center">
                <div
                  class="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-2xl flex items-center justify-center text-2xl font-bold shadow-lg group-hover:scale-110 transition-transform relative z-10">
                  2
                </div>
                <div
                  class="absolute inset-0 bg-indigo-400 rounded-2xl blur-xl opacity-20 group-hover:opacity-30 transition-opacity">
                </div>
              </div>
              <div class="bg-slate-50 rounded-xl p-6 h-full hover:shadow-lg transition-shadow border border-slate-200">
                <h3 class="text-xl font-bold text-slate-900 mb-3">Select Date & Time</h3>
                <p class="text-slate-600">Choose your preferred date and time slot that fits your schedule</p>
              </div>
            </div>

            <!-- Step 3 -->
            <div class="group text-center">
              <div class="relative mb-6 flex justify-center">
                <div
                  class="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-600 text-white rounded-2xl flex items-center justify-center text-2xl font-bold shadow-lg group-hover:scale-110 transition-transform relative z-10">
                  3
                </div>
                <div
                  class="absolute inset-0 bg-purple-400 rounded-2xl blur-xl opacity-20 group-hover:opacity-30 transition-opacity">
                </div>
              </div>
              <div class="bg-slate-50 rounded-xl p-6 h-full hover:shadow-lg transition-shadow border border-slate-200">
                <h3 class="text-xl font-bold text-slate-900 mb-3">Book Instantly</h3>
                <p class="text-slate-600">Complete secure payment and receive instant booking confirmation</p>
              </div>
            </div>

            <!-- Step 4 -->
            <div class="group text-center">
              <div class="relative mb-6 flex justify-center">
                <div
                  class="w-20 h-20 bg-gradient-to-br from-pink-500 to-rose-600 text-white rounded-2xl flex items-center justify-center text-2xl font-bold shadow-lg group-hover:scale-110 transition-transform relative z-10">
                  4
                </div>
                <div
                  class="absolute inset-0 bg-pink-400 rounded-2xl blur-xl opacity-20 group-hover:opacity-30 transition-opacity">
                </div>
              </div>
              <div class="bg-slate-50 rounded-xl p-6 h-full hover:shadow-lg transition-shadow border border-slate-200">
                <h3 class="text-xl font-bold text-slate-900 mb-3">Play & Enjoy</h3>
                <p class="text-slate-600">Show up and enjoy your game. Leave a review after your session</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Courts Section -->
    <section class="py-20 bg-gradient-to-br from-slate-50 to-blue-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between mb-12">
          <div>
            <span class="inline-block px-4 py-2 bg-blue-100 text-blue-600 rounded-full text-sm font-semibold mb-4">
              FEATURED COURTS
            </span>
            <h2 class="text-4xl lg:text-5xl font-bold text-slate-900 mb-2">Top-Rated Courts</h2>
            <p class="text-xl text-slate-600">Premium facilities in your area</p>
          </div>
          <router-link to="/courts"
            class="hidden md:flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold group">
            View All Courts
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor"
              viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>

        <div v-if="loading" class="flex justify-center py-20">
          <div class="relative">
            <div class="w-16 h-16 border-4 border-slate-200 border-t-blue-600 rounded-full animate-spin"></div>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="court in featuredCourts" :key="court.id"
            class="group bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-2xl transition-all cursor-pointer border border-slate-200 hover:-translate-y-1"
            @click="router.push(`/courts/${court.id}`)">
            <!-- Court Image -->
            <div class="relative h-52 overflow-hidden">
              <img v-if="court.primary_image" :src="court.primary_image" :alt="court.name"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300" />
              <div v-else
                class="w-full h-full bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 flex items-center justify-center">
                <svg class="w-20 h-20 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent"></div>
              <span
                class="absolute top-4 left-4 px-3 py-1.5 bg-white/90 backdrop-blur-sm text-blue-600 text-xs font-bold rounded-full shadow-lg">
                {{ court.category_name || court.court_type }}
              </span>
            </div>

            <!-- Court Info -->
            <div class="p-5">
              <div class="flex items-center gap-2 text-sm text-slate-500 mb-3">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ court.city }}
              </div>

              <h3 class="text-lg font-bold text-slate-900 mb-3 group-hover:text-blue-600 transition-colors">{{
                court.name }}</h3>

              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-1">
                  <svg class="w-5 h-5 text-amber-400 fill-current" viewBox="0 0 24 24">
                    <path
                      d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                  </svg>
                  <span class="font-bold text-slate-900">{{ court.average_rating || '4.8' }}</span>
                  <span class="text-slate-400 text-sm">(120)</span>
                </div>
                <span class="inline-flex items-center gap-1 text-sm text-emerald-600 font-semibold">
                  <span class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
                  Available
                </span>
              </div>

              <div class="flex items-center justify-between pt-4 border-t border-slate-200 mb-4">
                <div>
                  <p class="text-xs text-slate-500 mb-1">Starting from</p>
                  <p class="text-2xl font-bold text-blue-600">${{ court.base_hourly_rate }}<span
                      class="text-sm text-slate-500 font-normal">/hour</span></p>
                </div>
              </div>

              <button
                class="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition-all shadow-md hover:shadow-lg">
                Book Now
              </button>
            </div>
          </div>
        </div>

        <div class="mt-8 text-center md:hidden">
          <router-link to="/courts"
            class="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold">
            View All Courts
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Stats Section with Modern Design -->
    <section class="py-20 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 relative overflow-hidden">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center text-white">
          <div class="group">
            <div
              class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 group-hover:bg-white/20 transition-all">
              <p class="text-5xl lg:text-6xl font-bold mb-2">500+</p>
              <p class="text-lg text-blue-100">Active Courts</p>
            </div>
          </div>
          <div class="group">
            <div
              class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 group-hover:bg-white/20 transition-all">
              <p class="text-5xl lg:text-6xl font-bold mb-2">25K+</p>
              <p class="text-lg text-blue-100">Happy Users</p>
            </div>
          </div>
          <div class="group">
            <div
              class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 group-hover:bg-white/20 transition-all">
              <p class="text-5xl lg:text-6xl font-bold mb-2">100K+</p>
              <p class="text-lg text-blue-100">Bookings Made</p>
            </div>
          </div>
          <div class="group">
            <div
              class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 group-hover:bg-white/20 transition-all">
              <p class="text-5xl lg:text-6xl font-bold mb-2">50+</p>
              <p class="text-lg text-blue-100">Cities Served</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <span class="inline-block px-4 py-2 bg-blue-100 text-blue-600 rounded-full text-sm font-semibold mb-4">
            WHY CHOOSE US
          </span>
          <h2 class="text-4xl lg:text-5xl font-bold text-slate-900 mb-4">The BookACourt Advantage</h2>
          <p class="text-xl text-slate-600 max-w-2xl mx-auto">Everything you need for the perfect sports booking
            experience</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div
            class="group text-center p-8 bg-gradient-to-br from-slate-50 to-blue-50 rounded-2xl hover:shadow-xl transition-all border border-slate-200">
            <div
              class="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">Instant Booking</h3>
            <p class="text-slate-600">Book your favorite court in seconds with our lightning-fast interface</p>
          </div>

          <div
            class="group text-center p-8 bg-gradient-to-br from-slate-50 to-indigo-50 rounded-2xl hover:shadow-xl transition-all border border-slate-200">
            <div
              class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">Active Community</h3>
            <p class="text-slate-600">Connect with sports enthusiasts and find teammates in your area</p>
          </div>

          <div
            class="group text-center p-8 bg-gradient-to-br from-slate-50 to-purple-50 rounded-2xl hover:shadow-xl transition-all border border-slate-200">
            <div
              class="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">Secure Payments</h3>
            <p class="text-slate-600">Safe and encrypted payment options for every transaction</p>
          </div>

          <div
            class="group text-center p-8 bg-gradient-to-br from-slate-50 to-pink-50 rounded-2xl hover:shadow-xl transition-all border border-slate-200">
            <div
              class="w-16 h-16 bg-gradient-to-br from-pink-500 to-rose-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">Premium Quality</h3>
            <p class="text-slate-600">Access top-rated courts with professional-grade facilities</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Special Offers Section -->
    <section class="py-20 bg-gradient-to-br from-slate-50 to-blue-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <span class="inline-block px-4 py-2 bg-amber-100 text-amber-600 rounded-full text-sm font-semibold mb-4">
            SPECIAL OFFERS
          </span>
          <h2 class="text-4xl lg:text-5xl font-bold text-slate-900 mb-4">Exclusive Deals & Rewards</h2>
          <p class="text-xl text-slate-600">Get more value with our special promotions</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Offer 1 -->
          <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-200 hover:shadow-xl transition-all group">
            <div
              class="w-14 h-14 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-900 mb-3">20% Off First Booking</h3>
            <p class="text-slate-600 mb-6">New members get 20% discount on their first court booking. Use code <span
                class="font-mono font-semibold text-blue-600">NEWCOURT20</span> at checkout.</p>
            <p class="text-sm text-slate-500">Valid until Dec 31, 2025</p>
          </div>

          <!-- Offer 2 -->
          <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-200 hover:shadow-xl transition-all group">
            <div
              class="w-14 h-14 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-900 mb-3">Loyalty Rewards</h3>
            <p class="text-slate-600 mb-6">Earn points on every booking and redeem them for discounts on future
              reservations. The more you play, the more you save!</p>
            <p class="text-sm text-slate-500">Available for all members</p>
          </div>

          <!-- Offer 3 -->
          <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-200 hover:shadow-xl transition-all group">
            <div
              class="w-14 h-14 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-900 mb-3">Group Bookings</h3>
            <p class="text-slate-600 mb-6">Book 5+ courts and get special group rates. Perfect for tournaments,
              corporate events, and team gatherings.</p>
            <p class="text-sm text-slate-500">Contact support for details</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <span class="inline-block px-4 py-2 bg-blue-100 text-blue-600 rounded-full text-sm font-semibold mb-4">
            TESTIMONIALS
          </span>
          <h2 class="text-4xl lg:text-5xl font-bold text-slate-900 mb-4">What Players Say</h2>
          <p class="text-xl text-slate-600">Trusted by thousands of athletes</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div
            class="bg-gradient-to-br from-slate-50 to-blue-50 p-8 rounded-2xl border border-slate-200 hover:shadow-xl transition-all">
            <div class="flex gap-1 mb-6">
              <svg v-for="i in 5" :key="i" class="w-6 h-6 text-amber-400 fill-current" viewBox="0 0 24 24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
            <p class="text-slate-700 text-lg italic mb-6 leading-relaxed">"BookACourt made finding the perfect court so
              easy. The booking process is seamless and the courts are top quality. Best app for sports facilities!"</p>
            <div class="flex items-center gap-4 pt-6 border-t border-slate-200">
              <div
                class="w-12 h-12 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                AJ
              </div>
              <div>
                <p class="font-bold text-slate-900">Alex Johnson</p>
                <p class="text-sm text-slate-500">Basketball Enthusiast</p>
              </div>
            </div>
          </div>

          <div
            class="bg-gradient-to-br from-slate-50 to-indigo-50 p-8 rounded-2xl border border-slate-200 hover:shadow-xl transition-all">
            <div class="flex gap-1 mb-6">
              <svg v-for="i in 5" :key="i" class="w-6 h-6 text-amber-400 fill-current" viewBox="0 0 24 24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
            <p class="text-slate-700 text-lg italic mb-6 leading-relaxed">"Great experience from booking to payment. The
              courts are well-maintained and the staff is helpful. Highly recommend BookACourt to all players."</p>
            <div class="flex items-center gap-4 pt-6 border-t border-slate-200">
              <div
                class="w-12 h-12 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                SW
              </div>
              <div>
                <p class="font-bold text-slate-900">Sarah Williams</p>
                <p class="text-sm text-slate-500">Football Player</p>
              </div>
            </div>
          </div>

          <div
            class="bg-gradient-to-br from-slate-50 to-purple-50 p-8 rounded-2xl border border-slate-200 hover:shadow-xl transition-all">
            <div class="flex gap-1 mb-6">
              <svg v-for="i in 5" :key="i" class="w-6 h-6 text-amber-400 fill-current" viewBox="0 0 24 24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
            <p class="text-slate-700 text-lg italic mb-6 leading-relaxed">"Professional courts and reliable booking
              system. I use it for all my team practices and tournaments. Perfect for organizing events!"</p>
            <div class="flex items-center gap-4 pt-6 border-t border-slate-200">
              <div
                class="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                MC
              </div>
              <div>
                <p class="font-bold text-slate-900">Mike Chen</p>
                <p class="text-sm text-slate-500">Futsal Coach</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Community Section -->
    <section class="py-20 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 relative overflow-hidden">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="absolute top-0 right-0 -translate-y-12 translate-x-12 blur-3xl opacity-20">
        <div class="w-96 h-96 bg-cyan-400 rounded-full"></div>
      </div>
      <div class="absolute bottom-0 left-0 translate-y-12 -translate-x-12 blur-3xl opacity-20">
        <div class="w-96 h-96 bg-pink-400 rounded-full"></div>
      </div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-4xl lg:text-5xl font-bold text-white mb-4">Join Our Community</h2>
          <p class="text-xl text-blue-100 max-w-2xl mx-auto">More than just booking. A vibrant community of athletes,
            fitness enthusiasts, and sports lovers.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div
            class="text-center bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition-all">
            <div
              class="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white mb-3">Active Community</h3>
            <p class="text-blue-100 mb-4">Join thousands of sports enthusiasts in your area</p>
            <span class="inline-block px-4 py-2 bg-emerald-500 text-white rounded-full text-sm font-bold">50K+ Active
              Members</span>
          </div>

          <div
            class="text-center bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition-all">
            <div
              class="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white mb-3">Tournaments & Events</h3>
            <p class="text-blue-100 mb-4">Participate in regular tournaments and competitions</p>
            <span class="inline-block px-4 py-2 bg-emerald-500 text-white rounded-full text-sm font-bold">100+
              Events/Month</span>
          </div>

          <div
            class="text-center bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition-all">
            <div
              class="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white mb-3">Local Connections</h3>
            <p class="text-blue-100 mb-4">Connect with players and teams near you</p>
            <span class="inline-block px-4 py-2 bg-emerald-500 text-white rounded-full text-sm font-bold">500+
              Cities</span>
          </div>
        </div>

        <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 lg:p-12 text-center">
          <h3 class="text-3xl font-bold text-white mb-4">Create Your Team</h3>
          <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">Organize your friends and teammates, manage bookings
            together, and track your game history.</p>
          <router-link to="/signup"
            class="inline-flex items-center gap-2 bg-white hover:bg-blue-50 text-blue-600 px-8 py-4 rounded-xl font-bold text-lg transition-all shadow-xl hover:shadow-2xl hover:scale-105">
            Get Started Free
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-br from-slate-900 to-slate-800 text-white relative overflow-hidden">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl lg:text-5xl font-bold mb-6">Ready to Book Your Court?</h2>
        <p class="text-xl text-slate-300 mb-10 leading-relaxed">Join thousands of players who trust BookACourt for their
          sports bookings</p>
        <div class="flex flex-wrap gap-4 justify-center">
          <router-link to="/courts"
            class="group inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8 py-4 rounded-xl font-bold text-lg transition-all shadow-xl hover:shadow-2xl">
            Browse All Courts
            <svg class="w-6 h-6 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor"
              viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
          <router-link to="/signup"
            class="inline-flex items-center gap-2 bg-white hover:bg-slate-100 text-slate-900 px-8 py-4 rounded-xl font-bold text-lg transition-all">
            Sign Up Free
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { courtService } from '@/services/courtService'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const featuredCourts = ref([])

const searchFilters = ref({
  sport: '',
  location: '',
  date: ''
})

const minDate = computed(() => {
  return new Date().toISOString().split('T')[0]
})

const handleSearch = () => {
  router.push({
    path: '/courts',
    query: searchFilters.value
  })
}

const loadFeaturedCourts = async () => {
  loading.value = true
  try {
    const response = await courtService.getCourts({ page_size: 4 })
    featuredCourts.value = response.results || response.slice(0, 4) || []
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
