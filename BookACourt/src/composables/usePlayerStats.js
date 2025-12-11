// src/composables/usePlayerStats.js
import { ref, computed } from 'vue';
import { userService } from '@/services/userService';

export function usePlayerStats(userId = null) {
    const stats = ref(null);
    const leaderboard = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const winRate = computed(() => {
        if (!stats.value || stats.value.total_matches_played === 0) return 0;
        return ((stats.value.matches_won / stats.value.total_matches_played) * 100).toFixed(1);
    });

    const averageRating = computed(() => {
        if (!stats.value) return 0;
        return parseFloat(stats.value.sportsmanship_rating || 0).toFixed(1);
    });

    const loadStats = async (playerId = userId) => {
        loading.value = true;
        error.value = null;
        try {
            if (playerId) {
                stats.value = await userService.getPlayerStatsById(playerId);
            } else {
                stats.value = await userService.getMyStats();
            }
        } catch (err) {
            console.error('Failed to load player stats:', err);
            error.value = 'Failed to load player stats';
        } finally {
            loading.value = false;
        }
    };

    const loadLeaderboard = async (params = {}) => {
        loading.value = true;
        error.value = null;
        try {
            const response = await userService.getLeaderboard(params);
            leaderboard.value = response.results || response;
        } catch (err) {
            console.error('Failed to load leaderboard:', err);
            error.value = 'Failed to load leaderboard';
        } finally {
            loading.value = false;
        }
    };

    const getPlayerRank = (playerId) => {
        const index = leaderboard.value.findIndex(p => p.player === playerId);
        return index !== -1 ? index + 1 : null;
    };

    const getStatsBadge = (stats) => {
        if (!stats) return { level: 'Beginner', color: 'gray' };

        const totalMatches = stats.total_matches_played;
        const winRate = stats.matches_won / Math.max(totalMatches, 1);
        const rating = parseFloat(stats.sportsmanship_rating || 0);

        if (totalMatches >= 100 && winRate >= 0.7 && rating >= 4.5) {
            return { level: 'Elite', color: 'purple' };
        } else if (totalMatches >= 50 && winRate >= 0.6 && rating >= 4.0) {
            return { level: 'Advanced', color: 'blue' };
        } else if (totalMatches >= 20 && winRate >= 0.5 && rating >= 3.5) {
            return { level: 'Intermediate', color: 'green' };
        } else {
            return { level: 'Beginner', color: 'gray' };
        }
    };

    return {
        stats,
        leaderboard,
        loading,
        error,
        winRate,
        averageRating,
        loadStats,
        loadLeaderboard,
        getPlayerRank,
        getStatsBadge
    };
}