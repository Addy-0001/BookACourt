<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">

        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Filter -->
            <div class="bg-white rounded-xl shadow-md p-4 mb-8">
                <div class="flex items-center gap-4 flex-wrap">
                    <label class="text-sm font-medium text-gray-700">Sort by:</label>
                    <select v-model="sortBy" @change="loadLeaderboard"
                        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="total_bookings">Total Bookings</option>
                        <option value="matches_won">Matches Won</option>
                        <option value="sportsmanship_rating">Rating</option>
                        <option value="total_matches_played">Matches Played</option>
                    </select>
                </div>
            </div>

            <!-- My Stats Card -->
            <div v-if="myStats"
                class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 mb-8 text-white">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-2xl font-bold">Your Stats</h2>
                    <span class="px-4 py-2 bg-white/20 backdrop-blur rounded-lg font-bold text-lg">
                        Rank #{{ myRank || '-' }}
                    </span>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div class="bg-white/10 backdrop-blur rounded-lg p-4">
                        <p class="text-sm opacity-90">Bookings</p>
                        <p class="text-2xl font-bold">{{ myStats.total_bookings || 0 }}</p>
                    </div>
                    <div class="bg-white/10 backdrop-blur rounded-lg p-4">
                        <p class="text-sm opacity-90">Matches Won</p>
                        <p class="text-2xl font-bold">{{ myStats.matches_won || 0 }}</p>
                    </div>
                    <div class="bg-white/10 backdrop-blur rounded-lg p-4">
                        <p class="text-sm opacity-90">Win Rate</p>
                        <p class="text-2xl font-bold">{{ winRate }}%</p>
                    </div>
                    <div class="bg-white/10 backdrop-blur rounded-lg p-4">
                        <p class="text-sm opacity-90">Rating</p>
                        <div class="flex items-center gap-1">
                            <svg class="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 24 24">
                                <path
                                    d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                            </svg>
                            <span class="text-2xl font-bold">{{ averageRating }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <!-- Error -->
            <div v-else-if="error" class="text-center py-20">
                <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-xl text-gray-600">{{ error }}</p>
            </div>

            <!-- Top 3 Podium -->
            <div v-else-if="leaderboard.length >= 3" class="mb-8">
                <div class="flex items-end justify-center gap-4">
                    <!-- Second Place -->
                    <div class="flex-1 max-w-xs">
                        <div
                            class="bg-white rounded-xl shadow-lg p-6 text-center border-t-4 border-gray-400 transform hover:scale-105 transition-transform">
                            <div
                                class="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-gray-300 to-gray-500 flex items-center justify-center text-white text-2xl font-bold">
                                {{ leaderboard[1].player_name.charAt(0).toUpperCase() }}
                            </div>
                            <div class="mb-2">
                                <span class="text-4xl font-bold text-gray-400">2</span>
                            </div>
                            <h3 class="font-bold text-lg text-gray-900 mb-1">{{ leaderboard[1].player_name }}</h3>
                            <p class="text-2xl font-bold text-blue-600">{{ getStatValue(leaderboard[1]) }}</p>
                            <p class="text-sm text-gray-600">{{ getStatLabel() }}</p>
                        </div>
                    </div>

                    <!-- First Place -->
                    <div class="flex-1 max-w-xs">
                        <div
                            class="bg-white rounded-xl shadow-xl p-6 text-center border-t-4 border-yellow-400 transform scale-110 hover:scale-115 transition-transform">
                            <div
                                class="w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-br from-yellow-300 to-yellow-600 flex items-center justify-center text-white text-3xl font-bold relative">
                                {{ leaderboard[0].player_name.charAt(0).toUpperCase() }}
                                <svg class="absolute -top-2 -right-2 w-8 h-8 text-yellow-500" fill="currentColor"
                                    viewBox="0 0 24 24">
                                    <path
                                        d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                                </svg>
                            </div>
                            <div class="mb-2">
                                <span class="text-5xl font-bold text-yellow-500">1</span>
                            </div>
                            <h3 class="font-bold text-xl text-gray-900 mb-1">{{ leaderboard[0].player_name }}</h3>
                            <p class="text-3xl font-bold text-blue-600">{{ getStatValue(leaderboard[0]) }}</p>
                            <p class="text-sm text-gray-600">{{ getStatLabel() }}</p>
                        </div>
                    </div>

                    <!-- Third Place -->
                    <div class="flex-1 max-w-xs">
                        <div
                            class="bg-white rounded-xl shadow-lg p-6 text-center border-t-4 border-amber-600 transform hover:scale-105 transition-transform">
                            <div
                                class="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-amber-400 to-amber-700 flex items-center justify-center text-white text-2xl font-bold">
                                {{ leaderboard[2].player_name.charAt(0).toUpperCase() }}
                            </div>
                            <div class="mb-2">
                                <span class="text-4xl font-bold text-amber-600">3</span>
                            </div>
                            <h3 class="font-bold text-lg text-gray-900 mb-1">{{ leaderboard[2].player_name }}</h3>
                            <p class="text-2xl font-bold text-blue-600">{{ getStatValue(leaderboard[2]) }}</p>
                            <p class="text-sm text-gray-600">{{ getStatLabel() }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Rest of Leaderboard -->
            <div v-if="leaderboard.length > 3" class="bg-white rounded-xl shadow-md overflow-hidden">
                <div class="divide-y divide-gray-200">
                    <div v-for="(player, index) in leaderboard.slice(3)" :key="player.id"
                        class="flex items-center gap-4 p-4 hover:bg-gray-50 transition-colors">
                        <div class="w-12 text-center">
                            <span class="text-lg font-bold text-gray-600">{{ index + 4 }}</span>
                        </div>
                        <div
                            class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-purple-400 flex items-center justify-center text-white font-bold">
                            {{ player.player_name.charAt(0).toUpperCase() }}
                        </div>
                        <div class="flex-1">
                            <h3 class="font-bold text-gray-900">{{ player.player_name }}</h3>
                            <p class="text-sm text-gray-600">
                                {{ player.total_matches_played || 0 }} matches played
                            </p>
                        </div>
                        <div class="text-right">
                            <p class="text-2xl font-bold text-blue-600">{{ getStatValue(player) }}</p>
                            <p class="text-xs text-gray-500">{{ getStatLabel() }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else-if="!loading && leaderboard.length === 0" class="text-center py-20">
                <svg class="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
                <p class="text-xl text-gray-600 mb-2">No data yet</p>
                <p class="text-gray-500">Start playing to see your stats!</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePlayerStats } from '@/composables/usePlayerStats'

const router = useRouter()
const {
    stats: myStats,
    leaderboard,
    loading,
    error,
    winRate,
    averageRating,
    loadStats,
    loadLeaderboard,
    getPlayerRank
} = usePlayerStats()

const sortBy = ref('total_bookings')

const myRank = computed(() => {
    if (!myStats.value) return null
    return getPlayerRank(myStats.value.player)
})

const getStatValue = (player) => {
    switch (sortBy.value) {
        case 'total_bookings':
            return player.total_bookings || 0
        case 'matches_won':
            return player.matches_won || 0
        case 'sportsmanship_rating':
            return parseFloat(player.sportsmanship_rating || 0).toFixed(1)
        case 'total_matches_played':
            return player.total_matches_played || 0
        default:
            return 0
    }
}

const getStatLabel = () => {
    const labels = {
        'total_bookings': 'bookings',
        'matches_won': 'wins',
        'sportsmanship_rating': 'rating',
        'total_matches_played': 'matches'
    }
    return labels[sortBy.value] || ''
}

const loadData = async () => {
    await loadStats()
    await loadLeaderboard({ ordering: `-${sortBy.value}` })
}

const goBack = () => router.go(-1)

onMounted(() => {
    loadData()
})
</script>