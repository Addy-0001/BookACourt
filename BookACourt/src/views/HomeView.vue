<template>
  <div class="min-h-screen bg-white">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-[#F3F4F6] to-[#E3F2FD] py-20 lg:py-32">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <!-- Left Content -->
          <div>
            <span class="inline-block px-4 py-2 bg-[#E3F2FD] text-[#0056B3] rounded-full text-sm font-medium mb-6">
              Your Sports Booking Platform
            </span>
            <h1 class="text-5xl lg:text-6xl font-bold text-[#1F2937] mb-6">
              Book Your Perfect Court
            </h1>
            <p class="text-lg text-[#9CA3AF] mb-8">
              Find and reserve premium football, basketball, and futsal courts in your area.
              Professional facilities. Instant confirmations. Seamless bookings.
            </p>
            <div class="flex flex-wrap gap-4">
              <router-link to="/courts"
                class="inline-flex items-center gap-2 bg-[#FF6B35] hover:bg-[#E55A2B] text-white px-8 py-4 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl">
                Browse Courts
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </router-link>
              <button
                class="inline-flex items-center gap-2 bg-white hover:bg-[#F3F4F6] text-[#1F2937] px-8 py-4 rounded-lg font-semibold transition-all border-2 border-[#E5E7EB]">
                Learn More
              </button>
            </div>
          </div>

          <!-- Right Image Placeholder -->
          <div class="hidden lg:block">
            <div
              class="bg-gradient-to-br from-[#E3F2FD] to-[#EDE9FE] rounded-2xl h-96 flex items-center justify-center">
              <svg class="w-32 h-32 text-[#9CA3AF]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Search Section -->
    <section class="py-12 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-[#1F2937] mb-3">Find Your Court</h2>
          <p class="text-[#9CA3AF]">Filter by sport, location, and date to find available courts</p>
        </div>

        <div class="bg-white rounded-xl shadow-lg p-6 border border-[#E5E7EB]">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-[#1F2937] mb-2">Sport Type</label>
              <select v-model="searchFilters.sport"
                class="w-full px-4 py-3 border border-[#E5E7EB] rounded-lg focus:ring-2 focus:ring-[#0056B3] focus:border-transparent">
                <option value="">All Sports</option>
                <option value="Basketball">Basketball</option>
                <option value="Football">Football</option>
                <option value="Futsal">Futsal</option>
                <option value="Tennis">Tennis</option>
                <option value="Badminton">Badminton</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-[#1F2937] mb-2">Location</label>
              <input v-model="searchFilters.location" type="text" placeholder="Enter city or area"
                class="w-full px-4 py-3 border border-[#E5E7EB] rounded-lg focus:ring-2 focus:ring-[#0056B3] focus:border-transparent" />
            </div>

            <div>
              <label class="block text-sm font-medium text-[#1F2937] mb-2">Date</label>
              <input v-model="searchFilters.date" type="date" :min="minDate"
                class="w-full px-4 py-3 border border-[#E5E7EB] rounded-lg focus:ring-2 focus:ring-[#0056B3] focus:border-transparent" />
            </div>

            <div class="flex items-end">
              <button @click="handleSearch"
                class="w-full py-3 bg-[#FF6B35] hover:bg-[#E55A2B] text-white rounded-lg font-semibold transition-all flex items-center justify-center gap-2">
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

    <!-- Stats Section -->
    <section class="py-16 bg-[#0056B3]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center text-white">
          <div>
            <p class="text-5xl font-bold mb-2">500+</p>
            <p class="text-lg opacity-90">Active Courts</p>
          </div>
          <div>
            <p class="text-5xl font-bold mb-2">25K+</p>
            <p class="text-lg opacity-90">Happy Users</p>
          </div>
          <div>
            <p class="text-5xl font-bold mb-2">100K+</p>
            <p class="text-lg opacity-90">Bookings Made</p>
          </div>
          <div>
            <p class="text-5xl font-bold mb-2">50+</p>
            <p class="text-lg opacity-90">Cities Served</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-[#1F2937] mb-4">How It Works</h2>
          <p class="text-lg text-[#9CA3AF]">Book your perfect court in 4 simple steps</p>
        </div>

        <div class="relative">
          <!-- Connection Line -->
          <div class="hidden lg:block absolute top-8 left-0 right-0 h-1 bg-[#E3F2FD]"></div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 relative">
            <!-- Step 1 -->
            <div class="text-center">
              <div
                class="w-16 h-16 bg-[#0056B3] text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6 relative z-10">
                1
              </div>
              <h3 class="text-xl font-bold text-[#1F2937] mb-3">Search & Explore</h3>
              <p class="text-[#9CA3AF]">Browse available courts in your area with detailed information and reviews</p>
            </div>

            <!-- Step 2 -->
            <div class="text-center">
              <div
                class="w-16 h-16 bg-[#0056B3] text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6 relative z-10">
                2
              </div>
              <h3 class="text-xl font-bold text-[#1F2937] mb-3">Select Date & Time</h3>
              <p class="text-[#9CA3AF]">Choose your preferred date and time slot that fits your schedule</p>
            </div>

            <!-- Step 3 -->
            <div class="text-center">
              <div
                class="w-16 h-16 bg-[#0056B3] text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6 relative z-10">
                3
              </div>
              <h3 class="text-xl font-bold text-[#1F2937] mb-3">Book Instantly</h3>
              <p class="text-[#9CA3AF]">Complete secure payment and receive instant booking confirmation</p>
            </div>

            <!-- Step 4 -->
            <div class="text-center">
              <div
                class="w-16 h-16 bg-[#0056B3] text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6 relative z-10">
                4
              </div>
              <h3 class="text-xl font-bold text-[#1F2937] mb-3">Play & Enjoy</h3>
              <p class="text-[#9CA3AF]">Show up and enjoy your game. Leave a review after your session</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Courts Section -->
    <section class="py-20 bg-[#F3F4F6]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between mb-12">
          <div>
            <h2 class="text-4xl font-bold text-[#1F2937] mb-2">Featured Courts</h2>
            <p class="text-[#9CA3AF]">Top-rated courts in your area</p>
          </div>
          <router-link to="/courts" class="text-[#FF6B35] hover:text-[#E55A2B] font-semibold flex items-center gap-2">
            View All
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>

        <div v-if="loading" class="flex justify-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#0056B3]"></div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="court in featuredCourts" :key="court.id"
            class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow cursor-pointer"
            @click="router.push(`/courts/${court.id}`)">
            <!-- Court Image -->
            <div class="relative h-48 bg-gradient-to-br from-[#E3F2FD] to-[#EDE9FE]">
              <img v-if="court.primary_image" :src="court.primary_image" :alt="court.name"
                class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-20 h-20 text-[#9CA3AF]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <span class="absolute top-3 left-3 px-3 py-1 bg-[#FF6B35] text-white text-xs font-semibold rounded-full">
                {{ court.category_name || court.court_type }}
              </span>
            </div>

            <!-- Court Info -->
            <div class="p-4">
              <div class="flex items-center gap-2 text-sm text-[#9CA3AF] mb-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ court.city }}
              </div>

              <h3 class="text-lg font-bold text-[#1F2937] mb-2">{{ court.name }}</h3>

              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-1">
                  <svg class="w-5 h-5 text-[#F59E0B]" fill="currentColor" viewBox="0 0 24 24">
                    <path
                      d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                  </svg>
                  <span class="font-semibold text-[#1F2937]">{{ court.average_rating || '4.8' }}</span>
                </div>
                <span class="text-sm text-[#0056B3] font-semibold">Available Today</span>
              </div>

              <div class="flex items-center justify-between pt-3 border-t border-[#E5E7EB]">
                <span class="text-2xl font-bold text-[#FF6B35]">${{ court.base_hourly_rate }}/hour</span>
              </div>

              <button
                class="w-full mt-3 py-2 bg-[#0056B3] hover:bg-[#003D82] text-white rounded-lg font-semibold transition-all">
                Book Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-[#1F2937] mb-4">Why Choose BookACourt?</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div class="text-center p-6 bg-[#F3F4F6] rounded-xl">
            <div class="w-16 h-16 bg-[#FEE2E2] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-[#EF4444]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Easy Booking</h3>
            <p class="text-[#9CA3AF]">Book your favorite court in seconds with our intuitive interface</p>
          </div>

          <div class="text-center p-6 bg-[#F3F4F6] rounded-xl">
            <div class="w-16 h-16 bg-[#FEE2E2] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-[#EF4444]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Community</h3>
            <p class="text-[#9CA3AF]">Connect with other sports enthusiasts and find teammates</p>
          </div>

          <div class="text-center p-6 bg-[#F3F4F6] rounded-xl">
            <div class="w-16 h-16 bg-[#FEE2E2] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-[#EF4444]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Secure Payments</h3>
            <p class="text-[#9CA3AF]">Safe and secure payment options for every transaction</p>
          </div>

          <div class="text-center p-6 bg-[#F3F4F6] rounded-xl">
            <div class="w-16 h-16 bg-[#FEE2E2] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-[#EF4444]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Premium Quality</h3>
            <p class="text-[#9CA3AF]">Access top-rated courts with professional facilities</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Special Offers Section -->
    <section class="py-20 bg-gradient-to-br from-[#E3F2FD] to-[#EDE9FE]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-[#1F2937] mb-4">Special Offers & Promotions</h2>
          <p class="text-[#9CA3AF]">Get exclusive deals and rewards when you book with us</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Offer 1 -->
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="w-12 h-12 bg-[#FEF3C7] rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-[#F59E0B]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">20% Off First Booking</h3>
            <p class="text-[#9CA3AF] mb-4">New members get 20% discount on their first court booking. Use code
              NEWCOURT20 at checkout.</p>
            <p class="text-sm text-[#9CA3AF]">Valid until Dec 31, 2025</p>
          </div>

          <!-- Offer 2 -->
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="w-12 h-12 bg-[#D1FAE5] rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-[#10B981]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Loyalty Rewards</h3>
            <p class="text-[#9CA3AF] mb-4">Earn points on every booking and redeem them for discounts on future
              reservations.</p>
            <p class="text-sm text-[#9CA3AF]">Available for all members</p>
          </div>

          <!-- Offer 3 -->
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="w-12 h-12 bg-[#E3F2FD] rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-[#0056B3]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Group Bookings</h3>
            <p class="text-[#9CA3AF] mb-4">Book 5+ courts and get special group rates. Perfect for tournaments and
              events.</p>
            <p class="text-sm text-[#9CA3AF]">Contact support for details</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-[#1F2937] mb-4">What Users Say</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-[#F3F4F6] p-6 rounded-xl">
            <div class="flex gap-1 mb-4">
              <svg v-for="i in 5" :key="i" class="w-5 h-5 text-[#F59E0B]" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
            <p class="text-[#1F2937] italic mb-4">"BookACourt made finding the perfect court so easy. Best app for
              booking sports facilities!"</p>
            <div class="border-t border-[#E5E7EB] pt-4">
              <p class="font-bold text-[#1F2937]">Alex Johnson</p>
              <p class="text-sm text-[#9CA3AF]">Basketball Enthusiast</p>
            </div>
          </div>

          <div class="bg-[#F3F4F6] p-6 rounded-xl">
            <div class="flex gap-1 mb-4">
              <svg v-for="i in 5" :key="i" class="w-5 h-5 text-[#F59E0B]" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
            <p class="text-[#1F2937] italic mb-4">"Great experience from booking to payment. Highly recommend BookACourt
              to all players."</p>
            <div class="border-t border-[#E5E7EB] pt-4">
              <p class="font-bold text-[#1F2937]">Sarah Williams</p>
              <p class="text-sm text-[#9CA3AF]">Football Player</p>
            </div>
          </div>

          <div class="bg-[#F3F4F6] p-6 rounded-xl">
            <div class="flex gap-1 mb-4">
              <svg v-for="i in 5" :key="i" class="w-5 h-5 text-[#F59E0B]" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
            <p class="text-[#1F2937] italic mb-4">"Professional courts and reliable booking system. Perfect for
              organizing tournaments."</p>
            <div class="border-t border-[#E5E7EB] pt-4">
              <p class="font-bold text-[#1F2937]">Mike Chen</p>
              <p class="text-sm text-[#9CA3AF]">Futsal Coach</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Community Section -->
    <section class="py-20 bg-gradient-to-br from-[#F3F4F6] to-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-[#1F2937] mb-4">Join Our Community</h2>
          <p class="text-[#9CA3AF] text-lg">BookACourt is more than just booking. It's a vibrant community of athletes,
            fitness enthusiasts, and sports lovers.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div class="text-center">
            <div class="w-20 h-20 bg-[#E3F2FD] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-10 h-10 text-[#0056B3]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Active Community</h3>
            <p class="text-[#9CA3AF] mb-4">Join thousands of sports enthusiasts in your area</p>
            <span class="inline-block px-4 py-2 bg-[#D1FAE5] text-[#10B981] rounded-full text-sm font-semibold">50K+
              Active Members</span>
          </div>

          <div class="text-center">
            <div class="w-20 h-20 bg-[#E3F2FD] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-10 h-10 text-[#0056B3]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Tournaments & Events</h3>
            <p class="text-[#9CA3AF] mb-4">Participate in regular tournaments and competitions</p>
            <span class="inline-block px-4 py-2 bg-[#D1FAE5] text-[#10B981] rounded-full text-sm font-semibold">100+
              Events/Month</span>
          </div>

          <div class="text-center">
            <div class="w-20 h-20 bg-[#E3F2FD] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-10 h-10 text-[#0056B3]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-[#1F2937] mb-2">Local Connections</h3>
            <p class="text-[#9CA3AF] mb-4">Connect with players and teams near you</p>
            <span class="inline-block px-4 py-2 bg-[#D1FAE5] text-[#10B981] rounded-full text-sm font-semibold">500+
              Cities Covered</span>
          </div>
        </div>

        <div class="bg-gradient-to-r from-[#E3F2FD] to-[#EDE9FE] rounded-2xl p-8 text-center">
          <h3 class="text-2xl font-bold text-[#1F2937] mb-3">Create Your Team</h3>
          <p class="text-[#9CA3AF] mb-6">Organize your friends and teammates, manage bookings together, and track your
            game history.</p>
          <router-link to="/signup"
            class="inline-flex items-center gap-2 bg-[#FF6B35] hover:bg-[#E55A2B] text-white px-8 py-3 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl">
            Get Started
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-r from-[#0056B3] to-[#003D82] text-white">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl font-bold mb-4">Ready to Book Your Court?</h2>
        <p class="text-xl mb-8 opacity-90">Join thousands of players who trust BookACourt for their sports bookings</p>
        <div class="flex flex-wrap gap-4 justify-center">
          <router-link to="/courts"
            class="inline-flex items-center gap-2 bg-[#FF6B35] hover:bg-[#E55A2B] text-white px-8 py-4 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl">
            Browse Courts
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
          <router-link to="/signup"
            class="inline-flex items-center gap-2 bg-white hover:bg-gray-100 text-[#0056B3] px-8 py-4 rounded-lg font-semibold transition-all">
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