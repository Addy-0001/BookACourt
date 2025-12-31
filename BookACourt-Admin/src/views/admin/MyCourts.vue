<template>
    <div class="my-courts-page">
        <!-- Page Header -->
        <div class="page-header">
            <div class="header-content">
                <h1>My Courts</h1>
                <p class="subtitle">Manage all your court facilities</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-primary" @click="navigateToCreate">
                    <span class="icon">➕</span>
                    <span>Add New Court</span>
                </button>
                <button class="btn btn-secondary" @click="refreshCourts">
                    <span class="icon">🔄</span>
                    <span>Refresh</span>
                </button>
            </div>
        </div>

        <!-- Filters Section -->
        <div class="filters-section">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input v-model="searchQuery" type="text" placeholder="Search courts by name, location, or type..."
                    @input="debouncedSearch" />
            </div>

            <div class="filter-group">
                <select v-model="filters.status" @change="applyFilters">
                    <option value="">All Status</option>
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                </select>

                <select v-model="filters.verified" @change="applyFilters">
                    <option value="">All Courts</option>
                    <option value="true">Verified</option>
                    <option value="false">Unverified</option>
                </select>

                <select v-model="filters.courtType" @change="applyFilters">
                    <option value="">All Types</option>
                    <option value="Basketball">Basketball</option>
                    <option value="Tennis">Tennis</option>
                    <option value="Badminton">Badminton</option>
                    <option value="Football">Football</option>
                    <option value="Volleyball">Volleyball</option>
                </select>

                <select v-model="filters.location" @change="applyFilters">
                    <option value="">All Locations</option>
                    <option value="indoor">Indoor</option>
                    <option value="outdoor">Outdoor</option>
                </select>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
            <div class="spinner"></div>
            <p>Loading your courts...</p>
        </div>

        <!-- Courts Grid -->
        <div v-else-if="filteredCourts.length > 0" class="courts-container">
            <div class="courts-grid">
                <div v-for="court in filteredCourts" :key="court.id" class="court-card">
                    <!-- Court Image -->
                    <div class="court-image">
                        <img v-if="court.primary_image" :src="court.primary_image" :alt="court.name" />
                        <div v-else class="court-placeholder">🏟️</div>
                        <div class="court-badges">
                            <span :class="['badge-status', court.is_active ? 'active' : 'inactive']">
                                {{ court.is_active ? 'Active' : 'Inactive' }}
                            </span>
                            <span v-if="court.is_verified" class="badge-verified">✓ Verified</span>
                        </div>
                    </div>

                    <!-- Court Content -->
                    <div class="court-content">
                        <div class="court-header">
                            <h3 class="court-name">{{ court.name }}</h3>
                            <div class="court-rating">
                                <span class="rating-stars">⭐</span>
                                <span class="rating-value">{{ court.average_rating || 'N/A' }}</span>
                                <span class="rating-count">({{ court.total_reviews || 0 }})</span>
                            </div>
                        </div>

                        <div class="court-info">
                            <div class="info-item">
                                <span class="info-icon">📍</span>
                                <span>{{ court.city }}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-icon">🏀</span>
                                <span>{{ court.court_type }}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-icon">{{ court.is_indoor ? '🏠' : '☀️' }}</span>
                                <span>{{ court.is_indoor ? 'Indoor' : 'Outdoor' }}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-icon">💰</span>
                                <span>NPR {{ court.base_hourly_rate }}/hr</span>
                            </div>
                        </div>

                        <div class="court-stats-grid">
                            <div class="stat-box">
                                <span class="stat-label">Today</span>
                                <span class="stat-value">{{ getCourtBookings(court.id, 'today') }}</span>
                            </div>
                            <div class="stat-box">
                                <span class="stat-label">This Week</span>
                                <span class="stat-value">{{ getCourtBookings(court.id, 'week') }}</span>
                            </div>
                            <div class="stat-box">
                                <span class="stat-label">Revenue</span>
                                <span class="stat-value">{{ formatCurrency(getCourtRevenue(court.id)) }}</span>
                            </div>
                        </div>

                        <div class="court-actions">
                            <router-link :to="`/admin/courts/${court.id}`" class="btn-action primary">
                                <span>👁️</span>
                                <span>View Details</span>
                            </router-link>
                            <router-link :to="`/admin/courts/${court.id}/edit`" class="btn-action secondary">
                                <span>✏️</span>
                                <span>Edit</span>
                            </router-link>
                            <button class="btn-action" :class="court.is_active ? 'warning' : 'success'"
                                @click="toggleCourtStatus(court)">
                                <span>{{ court.is_active ? '⏸️' : '▶️' }}</span>
                                <span>{{ court.is_active ? 'Deactivate' : 'Activate' }}</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
            <div class="empty-icon">🏟️</div>
            <h3>No Courts Found</h3>
            <p v-if="searchQuery || hasActiveFilters">
                No courts match your search criteria. Try adjusting your filters.
            </p>
            <p v-else>
                You haven't added any courts yet. Start by registering your first court facility.
            </p>
            <button class="btn btn-primary" @click="navigateToCreate" style="margin-top: 1.5rem;">
                <span>➕</span>
                <span>Add Your First Court</span>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAdminStore } from '@/stores/admin';

const router = useRouter();
const adminStore = useAdminStore();

// State
const loading = ref(false);
const searchQuery = ref('');
const filters = ref({
    status: '',
    verified: '',
    courtType: '',
    location: '',
});

// Computed
const hasActiveFilters = computed(() => {
    return filters.value.status || filters.value.verified ||
        filters.value.courtType || filters.value.location;
});

const filteredCourts = computed(() => {
    let courts = adminStore.courts;

    // Search filter
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        courts = courts.filter(c =>
            c.name.toLowerCase().includes(query) ||
            c.city.toLowerCase().includes(query) ||
            c.court_type.toLowerCase().includes(query)
        );
    }

    // Status filter
    if (filters.value.status === 'active') {
        courts = courts.filter(c => c.is_active);
    } else if (filters.value.status === 'inactive') {
        courts = courts.filter(c => !c.is_active);
    }

    // Verified filter
    if (filters.value.verified === 'true') {
        courts = courts.filter(c => c.is_verified);
    } else if (filters.value.verified === 'false') {
        courts = courts.filter(c => !c.is_verified);
    }

    // Court type filter
    if (filters.value.courtType) {
        courts = courts.filter(c => c.court_type === filters.value.courtType);
    }

    // Location filter
    if (filters.value.location === 'indoor') {
        courts = courts.filter(c => c.is_indoor);
    } else if (filters.value.location === 'outdoor') {
        courts = courts.filter(c => !c.is_indoor);
    }

    return courts;
});

// Lifecycle
onMounted(async () => {
    await loadCourts();
});

// Methods
async function loadCourts() {
    loading.value = true;
    try {
        await adminStore.fetchMyCourts();
    } catch (error) {
        console.error('Error loading courts:', error);
    } finally {
        loading.value = false;
    }
}

async function refreshCourts() {
    await loadCourts();
}

let searchTimeout;
function debouncedSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        // Search is reactive, no need to do anything
    }, 300);
}

function applyFilters() {
    // Filters are reactive, no need to do anything
}

function navigateToCreate() {
    router.push('/admin/courts/create');
}

async function toggleCourtStatus(court) {
    const action = court.is_active ? 'deactivate' : 'activate';
    if (!confirm(`Are you sure you want to ${action} "${court.name}"?`)) return;

    try {
        await adminStore.toggleCourtStatus(court.id, !court.is_active);
        alert(`✅ Court ${action}d successfully!`);
    } catch (error) {
        alert(`❌ Failed to ${action} court`);
    }
}

function getCourtBookings(courtId, period) {
    const bookings = adminStore.bookings.filter(b => b.court === courtId);

    if (period === 'today') {
        const today = new Date().toISOString().split('T')[0];
        return bookings.filter(b => b.booking_date === today).length;
    } else if (period === 'week') {
        const weekAgo = new Date();
        weekAgo.setDate(weekAgo.getDate() - 7);
        return bookings.filter(b => new Date(b.booking_date) >= weekAgo).length;
    }

    return bookings.length;
}

function getCourtRevenue(courtId) {
    return adminStore.bookings
        .filter(b => b.court === courtId && b.payment_status === 'COMPLETED')
        .reduce((sum, b) => sum + parseFloat(b.total_amount || 0), 0);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-NP', {
        maximumFractionDigits: 0
    }).format(amount);
}
</script>

<style scoped>
.my-courts-page {
    padding: 2rem;
    background: #f5f6fa;
    min-height: 100vh;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.header-content h1 {
    font-size: 2rem;
    color: #2c3e50;
    margin: 0 0 0.5rem 0;
    font-weight: 700;
}

.subtitle {
    color: #7f8c8d;
    margin: 0;
}

.header-actions {
    display: flex;
    gap: 1rem;
}

.btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.2s;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
    background: white;
    color: #667eea;
    border: 2px solid #667eea;
}

.btn-secondary:hover {
    background: #667eea;
    color: white;
}

/* Filters */
.filters-section {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
}

.search-box {
    position: relative;
    margin-bottom: 1rem;
}

.search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.25rem;
    color: #7f8c8d;
}

.search-box input {
    width: 100%;
    padding: 0.875rem 1rem 0.875rem 3rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.2s;
}

.search-box input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-group {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
}

.filter-group select {
    padding: 0.75rem 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.9rem;
    background: white;
    cursor: pointer;
}

/* Courts Grid */
.courts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
}

.court-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
}

.court-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.court-image {
    position: relative;
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.court-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.court-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
    color: white;
}

.court-badges {
    position: absolute;
    top: 1rem;
    right: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.badge-status,
.badge-verified {
    padding: 0.375rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    backdrop-filter: blur(10px);
}

.badge-status.active {
    background: rgba(39, 174, 96, 0.9);
    color: white;
}

.badge-status.inactive {
    background: rgba(231, 76, 60, 0.9);
    color: white;
}

.badge-verified {
    background: rgba(52, 152, 219, 0.9);
    color: white;
}

/* Court Content */
.court-content {
    padding: 1.5rem;
}

.court-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 1rem;
}

.court-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.court-rating {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    font-size: 0.9rem;
}

.rating-value {
    font-weight: 600;
    color: #2c3e50;
}

.rating-count {
    color: #7f8c8d;
}

.court-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e9ecef;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: #2c3e50;
}

.court-stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.stat-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
}

.stat-label {
    font-size: 0.75rem;
    color: #7f8c8d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #2c3e50;
}

.court-actions {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
}

.btn-action {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.625rem 0.75rem;
    border: none;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
    color: inherit;
}

.btn-action.primary {
    background: #e3f2fd;
    color: #1976d2;
}

.btn-action.primary:hover {
    background: #1976d2;
    color: white;
}

.btn-action.secondary {
    background: #fff3cd;
    color: #856404;
}

.btn-action.secondary:hover {
    background: #ffc107;
    color: white;
}

.btn-action.success {
    background: #d4edda;
    color: #155724;
}

.btn-action.success:hover {
    background: #28a745;
    color: white;
}

.btn-action.warning {
    background: #fff3cd;
    color: #856404;
}

.btn-action.warning:hover {
    background: #ffc107;
    color: white;
}

/* Loading & Empty States */
.loading-container,
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.empty-state h3 {
    margin: 0 0 0.5rem 0;
    color: #2c3e50;
}

.empty-state p {
    color: #7f8c8d;
    max-width: 500px;
    margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
    .my-courts-page {
        padding: 1rem;
    }

    .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }

    .header-actions {
        width: 100%;
        flex-direction: column;
    }

    .btn {
        width: 100%;
        justify-content: center;
    }

    .courts-grid {
        grid-template-columns: 1fr;
    }

    .filter-group {
        grid-template-columns: 1fr;
    }
}
</style>