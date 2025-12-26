<template>
    <div class="bookings-page">
        <!-- Page Header -->
        <div class="page-header">
            <div class="header-content">
                <h1>Booking Management</h1>
                <p class="subtitle">View and manage all court bookings</p>
            </div>
            <div class="header-actions">
                <button v-if="isCourtOwnerOrManager" class="btn btn-primary" @click="showCreateModal = true">
                    <span class="icon">➕</span>
                    <span>New Booking</span>
                </button>
                <button class="btn btn-secondary" @click="exportBookings">
                    <span class="icon">📊</span>
                    <span>Export</span>
                </button>
                <button class="btn btn-secondary" @click="refreshBookings">
                    <span class="icon">🔄</span>
                    <span>Refresh</span>
                </button>
            </div>
        </div>

        <!-- Stats Overview -->
        <div class="stats-overview">
            <div class="stat-card">
                <div class="stat-icon pending">📋</div>
                <div class="stat-content">
                    <h3>{{ bookingStats.pending }}</h3>
                    <p>Pending</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon confirmed">✅</div>
                <div class="stat-content">
                    <h3>{{ bookingStats.confirmed }}</h3>
                    <p>Confirmed</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon completed">🏆</div>
                <div class="stat-content">
                    <h3>{{ bookingStats.completed }}</h3>
                    <p>Completed</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon cancelled">❌</div>
                <div class="stat-content">
                    <h3>{{ bookingStats.cancelled }}</h3>
                    <p>Cancelled</p>
                </div>
            </div>
        </div>

        <!-- Filters and Search -->
        <div class="filters-section">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input v-model="filters.search" type="text"
                    placeholder="Search by booking reference, player name, or court..." @input="debouncedSearch" />
            </div>

            <div class="filter-group">
                <select v-model="filters.status" @change="applyFilters">
                    <option value="">All Status</option>
                    <option value="PENDING">Pending</option>
                    <option value="CONFIRMED">Confirmed</option>
                    <option value="COMPLETED">Completed</option>
                    <option value="CANCELLED">Cancelled</option>
                    <option value="NO_SHOW">No Show</option>
                </select>

                <select v-if="managedCourts.length > 1" v-model="filters.court" @change="applyFilters">
                    <option value="">All Courts</option>
                    <option v-for="court in managedCourts" :key="court.id" :value="court.id">
                        {{ court.name }}
                    </option>
                </select>

                <select v-model="filters.payment_status" @change="applyFilters">
                    <option value="">All Payments</option>
                    <option value="PENDING">Payment Pending</option>
                    <option value="COMPLETED">Paid</option>
                    <option value="FAILED">Failed</option>
                    <option value="REFUNDED">Refunded</option>
                </select>

                <input v-model="filters.date_from" type="date" @change="applyFilters" placeholder="From Date" />

                <input v-model="filters.date_to" type="date" @change="applyFilters" placeholder="To Date" />

                <button class="btn-clear-filters" @click="clearFilters" v-if="hasActiveFilters">
                    <span>✕</span>
                    <span>Clear Filters</span>
                </button>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
            <div class="spinner"></div>
            <p>Loading bookings...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-container">
            <div class="error-icon">⚠️</div>
            <h3>Failed to Load Bookings</h3>
            <p>{{ error }}</p>
            <button class="btn btn-primary" @click="refreshBookings">Try Again</button>
        </div>

        <!-- Bookings Table -->
        <div v-else-if="bookings.length > 0" class="table-container">
            <table class="bookings-table">
                <thead>
                    <tr>
                        <th @click="sortBy('booking_reference')" class="sortable">
                            Reference
                            <span class="sort-icon">{{ getSortIcon('booking_reference') }}</span>
                        </th>
                        <th @click="sortBy('court_name')" class="sortable">
                            Court
                            <span class="sort-icon">{{ getSortIcon('court_name') }}</span>
                        </th>
                        <th @click="sortBy('player_name')" class="sortable">
                            Player
                            <span class="sort-icon">{{ getSortIcon('player_name') }}</span>
                        </th>
                        <th @click="sortBy('booking_date')" class="sortable">
                            Date & Time
                            <span class="sort-icon">{{ getSortIcon('booking_date') }}</span>
                        </th>
                        <th>Duration</th>
                        <th @click="sortBy('total_amount')" class="sortable">
                            Amount
                            <span class="sort-icon">{{ getSortIcon('total_amount') }}</span>
                        </th>
                        <th>Status</th>
                        <th>Payment</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="booking in bookings" :key="booking.id" @click="viewBookingDetails(booking)">
                        <td>
                            <span class="reference-badge">{{ booking.booking_reference }}</span>
                        </td>
                        <td>
                            <div class="court-cell">
                                <span class="court-name">{{ booking.court_name }}</span>
                            </div>
                        </td>
                        <td>
                            <div class="player-cell">
                                <span class="player-name">{{ booking.player_name }}</span>
                            </div>
                        </td>
                        <td>
                            <div class="datetime-cell">
                                <span class="date">{{ formatDate(booking.booking_date) }}</span>
                                <span class="time">{{ formatTime(booking.start_time) }} - {{
                                    formatTime(booking.end_time) }}</span>
                            </div>
                        </td>
                        <td>
                            <span class="duration">{{ calculateDuration(booking.start_time, booking.end_time) }}</span>
                        </td>
                        <td>
                            <div class="amount-cell">
                                <span class="amount">NPR {{ formatCurrency(booking.total_amount) }}</span>
                                <span v-if="booking.discount_amount > 0" class="discount">
                                    -{{ formatCurrency(booking.discount_amount) }}
                                </span>
                            </div>
                        </td>
                        <td>
                            <span :class="['status-badge', getStatusClass(booking.status)]">
                                {{ booking.status }}
                            </span>
                        </td>
                        <td>
                            <span :class="['payment-badge', getPaymentClass(booking.payment_status)]">
                                {{ booking.payment_status }}
                            </span>
                        </td>
                        <td @click.stop>
                            <div class="action-buttons">
                                <button v-if="booking.status === 'PENDING' && canConfirm" class="btn-action btn-confirm"
                                    @click="confirmBooking(booking)" title="Confirm">
                                    ✓
                                </button>
                                <button v-if="canCancel(booking)" class="btn-action btn-cancel"
                                    @click="cancelBooking(booking)" title="Cancel">
                                    ✕
                                </button>
                                <button class="btn-action btn-view" @click="viewBookingDetails(booking)"
                                    title="View Details">
                                    👁️
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
            <div class="empty-icon">📅</div>
            <h3>No Bookings Found</h3>
            <p>{{ getEmptyStateMessage() }}</p>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.total > pagination.pageSize" class="pagination">
            <button class="btn-page" @click="goToPage(pagination.page - 1)" :disabled="pagination.page === 1">
                ‹ Previous
            </button>

            <div class="page-numbers">
                <button v-for="page in visiblePages" :key="page"
                    :class="['btn-page-number', { active: page === pagination.page }]" @click="goToPage(page)"
                    :disabled="page === '...'">
                    {{ page }}
                </button>
            </div>

            <button class="btn-page" @click="goToPage(pagination.page + 1)" :disabled="pagination.page === totalPages">
                Next ›
            </button>

            <div class="page-info">
                Showing {{ startRecord }}-{{ endRecord }} of {{ pagination.total }}
            </div>
        </div>

        <!-- Modals would go here - truncated for space -->
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAdminStore } from '@/stores/admin';
import { bookingApi, courtApi } from '@/services/api';

const router = useRouter();
const adminStore = useAdminStore();

// State
const loading = ref(true);
const processing = ref(false);
const error = ref(null);
const bookings = ref([]);
const managedCourts = ref([]);
const selectedBooking = ref(null);
const showDetailsModal = ref(false);
const showCreateModal = ref(false);
const showCancelModal = ref(false);
const cancelReason = ref('');
const sortColumn = ref('booking_date');
const sortDirection = ref('desc');

// Filters
const filters = ref({
    search: '',
    status: '',
    court: '',
    payment_status: '',
    date_from: '',
    date_to: '',
});

// Pagination
const pagination = ref({
    page: 1,
    pageSize: 20,
    total: 0,
});

// Current User
const currentUser = computed(() => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
});

const isSuperUser = computed(() => currentUser.value?.role === 'SUPER_USER');
const isCourtOwner = computed(() => currentUser.value?.role === 'COURT_OWNER');
const isCourtManager = computed(() => currentUser.value?.role === 'COURT_MANAGER');
const isCourtOwnerOrManager = computed(() => isCourtOwner.value || isCourtManager.value);
const canConfirm = computed(() => isCourtOwnerOrManager.value || isSuperUser.value);

const today = computed(() => new Date().toISOString().split('T')[0]);

// Booking Stats
const bookingStats = computed(() => {
    return {
        pending: bookings.value.filter(b => b.status === 'PENDING').length,
        confirmed: bookings.value.filter(b => b.status === 'CONFIRMED').length,
        completed: bookings.value.filter(b => b.status === 'COMPLETED').length,
        cancelled: bookings.value.filter(b => b.status === 'CANCELLED').length,
    };
});

// Pagination computed
const totalPages = computed(() => Math.ceil(pagination.value.total / pagination.value.pageSize));
const startRecord = computed(() => (pagination.value.page - 1) * pagination.value.pageSize + 1);
const endRecord = computed(() => Math.min(pagination.value.page * pagination.value.pageSize, pagination.value.total));

const visiblePages = computed(() => {
    const pages = [];
    const current = pagination.value.page;
    const total = totalPages.value;

    if (total <= 7) {
        for (let i = 1; i <= total; i++) pages.push(i);
    } else {
        if (current <= 4) {
            for (let i = 1; i <= 5; i++) pages.push(i);
            pages.push('...');
            pages.push(total);
        } else if (current >= total - 3) {
            pages.push(1);
            pages.push('...');
            for (let i = total - 4; i <= total; i++) pages.push(i);
        } else {
            pages.push(1);
            pages.push('...');
            for (let i = current - 1; i <= current + 1; i++) pages.push(i);
            pages.push('...');
            pages.push(total);
        }
    }
    return pages;
});

const hasActiveFilters = computed(() => {
    return filters.value.search || filters.value.status || filters.value.court ||
        filters.value.payment_status || filters.value.date_from || filters.value.date_to;
});

// Lifecycle
onMounted(async () => {
    await loadManagedCourts();
    await loadBookings();
});

// Methods
async function loadManagedCourts() {
    try {
        if (isCourtOwnerOrManager.value) {
            const params = isCourtOwner.value
                ? { owner: currentUser.value.id }
                : { manager: currentUser.value.id };
            const response = await courtApi.getCourts(params);
            managedCourts.value = response.data.results || response.data;
        }
    } catch (err) {
        console.error('Error loading courts:', err);
    }
}

async function loadBookings() {
    loading.value = true;
    error.value = null;

    try {
        const params = {
            page: pagination.value.page,
            page_size: pagination.value.pageSize,
            ordering: sortDirection.value === 'desc' ? `-${sortColumn.value}` : sortColumn.value,
        };

        // Apply filters
        if (filters.value.search) params.search = filters.value.search;
        if (filters.value.status) params.status = filters.value.status;
        if (filters.value.court) params.court = filters.value.court;
        if (filters.value.payment_status) params.payment_status = filters.value.payment_status;
        if (filters.value.date_from) params.booking_date__gte = filters.value.date_from;
        if (filters.value.date_to) params.booking_date__lte = filters.value.date_to;

        // Filter by user's courts if not super user
        if (isCourtOwnerOrManager.value && managedCourts.value.length > 0 && !filters.value.court) {
            params.court__in = managedCourts.value.map(c => c.id).join(',');
        }

        const response = await bookingApi.getBookings(params);
        bookings.value = response.data.results || response.data;
        pagination.value.total = response.data.count || bookings.value.length;
    } catch (err) {
        error.value = err.response?.data?.message || 'Failed to load bookings';
        console.error('Load bookings error:', err);
    } finally {
        loading.value = false;
    }
}

async function refreshBookings() {
    pagination.value.page = 1;
    await loadBookings();
}

let searchTimeout;
function debouncedSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        pagination.value.page = 1;
        loadBookings();
    }, 500);
}

function applyFilters() {
    pagination.value.page = 1;
    loadBookings();
}

function clearFilters() {
    filters.value = {
        search: '',
        status: '',
        court: '',
        payment_status: '',
        date_from: '',
        date_to: '',
    };
    applyFilters();
}

function sortBy(column) {
    if (sortColumn.value === column) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
        sortColumn.value = column;
        sortDirection.value = 'asc';
    }
    loadBookings();
}

function getSortIcon(column) {
    if (sortColumn.value !== column) return '↕️';
    return sortDirection.value === 'asc' ? '↑' : '↓';
}

function goToPage(page) {
    if (page >= 1 && page <= totalPages.value && page !== '...') {
        pagination.value.page = page;
        loadBookings();
    }
}

async function confirmBooking(booking) {
    if (!confirm(`Confirm booking ${booking.booking_reference}?`)) return;

    processing.value = true;
    try {
        await bookingApi.confirmBooking(booking.id);
        await loadBookings();
        alert('✅ Booking confirmed successfully!');
    } catch (err) {
        alert('❌ Failed to confirm booking');
        console.error('Confirm error:', err);
    } finally {
        processing.value = false;
    }
}

function cancelBooking(booking) {
    selectedBooking.value = booking;
    cancelReason.value = '';
    showCancelModal.value = true;
}

async function confirmCancel() {
    if (!cancelReason.value.trim()) return;

    processing.value = true;
    try {
        await bookingApi.cancelBooking(selectedBooking.value.id, cancelReason.value);
        await loadBookings();
        showCancelModal.value = false;
        alert('✅ Booking cancelled successfully!');
    } catch (err) {
        alert('❌ Failed to cancel booking');
    } finally {
        processing.value = false;
    }
}

function canCancel(booking) {
    return (isCourtOwnerOrManager.value || isSuperUser.value) &&
        ['PENDING', 'CONFIRMED'].includes(booking.status);
}

function viewBookingDetails(booking) {
    selectedBooking.value = booking;
    showDetailsModal.value = true;
}

function exportBookings() {
    // Implementation for export
    alert('Export functionality will be implemented');
}

function getEmptyStateMessage() {
    if (hasActiveFilters.value) return 'No bookings match your filters. Try adjusting your search criteria.';
    return 'No bookings found. Bookings will appear here once customers make reservations.';
}

// Utility Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-NP').format(amount);
}

function calculateDuration(startTime, endTime) {
    const [startHours, startMinutes] = startTime.split(':').map(Number);
    const [endHours, endMinutes] = endTime.split(':').map(Number);
    const startTotalMinutes = startHours * 60 + startMinutes;
    const endTotalMinutes = endHours * 60 + endMinutes;
    const durationMinutes = endTotalMinutes - startTotalMinutes;
    const hours = Math.floor(durationMinutes / 60);
    const minutes = durationMinutes % 60;
    return `${hours}h ${minutes}m`;
}

function getStatusClass(status) {
    const statusMap = {
        PENDING: 'pending',
        CONFIRMED: 'confirmed',
        CANCELLED: 'cancelled',
        COMPLETED: 'completed',
        NO_SHOW: 'no-show',
    };
    return statusMap[status] || 'pending';
}

function getPaymentClass(status) {
    const statusMap = {
        PENDING: 'pending',
        COMPLETED: 'completed',
        REFUNDED: 'refunded',
        FAILED: 'failed',
    };
    return statusMap[status] || 'pending';
}
</script>

<style scoped>
/* BookingsView.vue Styles */

.bookings-page {
    padding: 2rem;
    background: #f5f6fa;
    min-height: 100vh;
}

/* Page Header */
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
    font-size: 1rem;
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
    white-space: nowrap;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
    background: white;
    color: #667eea;
    border: 2px solid #667eea;
}

.btn-secondary:hover:not(:disabled) {
    background: #667eea;
    color: white;
}

.btn-success {
    background: #27ae60;
    color: white;
}

.btn-success:hover:not(:disabled) {
    background: #229954;
    transform: translateY(-2px);
}

.btn-danger {
    background: #e74c3c;
    color: white;
}

.btn-danger:hover:not(:disabled) {
    background: #c0392b;
    transform: translateY(-2px);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.icon {
    font-size: 1.1rem;
}

/* Stats Overview */
.stats-overview {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.stat-icon {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.stat-icon.pending {
    background: #fff3cd;
    color: #856404;
}

.stat-icon.confirmed {
    background: #d4edda;
    color: #155724;
}

.stat-icon.completed {
    background: #d1ecf1;
    color: #0c5460;
}

.stat-icon.cancelled {
    background: #f8d7da;
    color: #721c24;
}

.stat-content h3 {
    font-size: 2rem;
    font-weight: 700;
    color: #2c3e50;
    margin: 0;
}

.stat-content p {
    font-size: 0.9rem;
    color: #7f8c8d;
    margin: 0.25rem 0 0 0;
}

/* Filters Section */
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
    pointer-events: none;
}

.search-box input {
    width: 100%;
    padding: 0.875rem 1rem 0.875rem 3rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.2s;
    font-family: inherit;
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

.filter-group select,
.filter-group input[type="date"] {
    padding: 0.75rem 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.9rem;
    transition: all 0.2s;
    font-family: inherit;
    background: white;
}

.filter-group select:focus,
.filter-group input[type="date"]:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-clear-filters {
    padding: 0.75rem 1rem;
    background: #fee;
    color: #c0392b;
    border: 2px solid #f8d7da;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    white-space: nowrap;
}

.btn-clear-filters:hover {
    background: #f8d7da;
    border-color: #e74c3c;
}

/* Loading State */
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.loading-container p {
    color: #7f8c8d;
    margin: 0;
}

/* Error State */
.error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.error-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #e74c3c;
}

.error-container h3 {
    color: #2c3e50;
    margin: 0 0 0.5rem 0;
}

.error-container p {
    color: #7f8c8d;
    margin: 0 0 1.5rem 0;
}

/* Table Container */
.table-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    margin-bottom: 2rem;
}

.bookings-table {
    width: 100%;
    border-collapse: collapse;
}

.bookings-table thead {
    background: #f8f9fa;
    border-bottom: 2px solid #e9ecef;
}

.bookings-table th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    color: #2c3e50;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
}

.bookings-table th.sortable {
    cursor: pointer;
    user-select: none;
    transition: background 0.2s;
}

.bookings-table th.sortable:hover {
    background: #e9ecef;
}

.sort-icon {
    margin-left: 0.5rem;
    opacity: 0.5;
    font-size: 0.8rem;
}

.bookings-table tbody tr {
    border-bottom: 1px solid #f8f9fa;
    transition: background 0.2s;
    cursor: pointer;
}

.bookings-table tbody tr:hover {
    background: #f8f9fa;
}

.bookings-table td {
    padding: 1rem;
    color: #2c3e50;
    font-size: 0.9rem;
}

/* Table Cell Styles */
.reference-badge {
    display: inline-block;
    padding: 0.375rem 0.75rem;
    background: #e3f2fd;
    color: #1976d2;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.85rem;
    font-family: 'Courier New', monospace;
}

.court-cell,
.player-cell {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.court-name,
.player-name {
    font-weight: 500;
    color: #2c3e50;
}

.datetime-cell {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.datetime-cell .date {
    font-weight: 500;
    color: #2c3e50;
}

.datetime-cell .time {
    font-size: 0.85rem;
    color: #7f8c8d;
}

.duration {
    font-weight: 500;
    color: #7f8c8d;
}

.amount-cell {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.amount {
    font-weight: 600;
    color: #2c3e50;
}

.discount {
    font-size: 0.85rem;
    color: #e74c3c;
    font-weight: 500;
}

/* Status Badges */
.status-badge,
.payment-badge {
    display: inline-block;
    padding: 0.375rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
    white-space: nowrap;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-badge.pending {
    background: #fff3cd;
    color: #856404;
}

.status-badge.confirmed {
    background: #d4edda;
    color: #155724;
}

.status-badge.cancelled {
    background: #f8d7da;
    color: #721c24;
}

.status-badge.completed {
    background: #d1ecf1;
    color: #0c5460;
}

.status-badge.no-show {
    background: #e2e3e5;
    color: #383d41;
}

.payment-badge.pending {
    background: #fff3cd;
    color: #856404;
}

.payment-badge.completed {
    background: #d4edda;
    color: #155724;
}

.payment-badge.failed {
    background: #f8d7da;
    color: #721c24;
}

.payment-badge.refunded {
    background: #d1ecf1;
    color: #0c5460;
}

/* Action Buttons */
.action-buttons {
    display: flex;
    gap: 0.5rem;
}

.btn-action {
    width: 32px;
    height: 32px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-confirm {
    background: #d4edda;
    color: #155724;
}

.btn-confirm:hover {
    background: #27ae60;
    color: white;
    transform: scale(1.1);
}

.btn-cancel {
    background: #f8d7da;
    color: #721c24;
}

.btn-cancel:hover {
    background: #e74c3c;
    color: white;
    transform: scale(1.1);
}

.btn-view {
    background: #e3f2fd;
    color: #1976d2;
}

.btn-view:hover {
    background: #2196f3;
    color: white;
    transform: scale(1.1);
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.empty-state h3 {
    margin: 0 0 0.5rem 0;
    color: #2c3e50;
    font-size: 1.5rem;
}

.empty-state p {
    color: #7f8c8d;
    margin: 0;
    max-width: 500px;
    margin: 0 auto;
}

/* Pagination */
.pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 2rem 0;
    flex-wrap: wrap;
}

.btn-page {
    padding: 0.625rem 1rem;
    background: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    color: #2c3e50;
    transition: all 0.2s;
}

.btn-page:hover:not(:disabled) {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.btn-page:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.page-numbers {
    display: flex;
    gap: 0.5rem;
}

.btn-page-number {
    width: 40px;
    height: 40px;
    padding: 0;
    background: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    color: #2c3e50;
    transition: all 0.2s;
}

.btn-page-number:hover:not(:disabled) {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.btn-page-number.active {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.btn-page-number:disabled {
    cursor: default;
    border: none;
    background: transparent;
}

.page-info {
    color: #7f8c8d;
    font-size: 0.9rem;
}

/* Modal Overlay */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: fadeIn 0.2s;
    padding: 1rem;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

/* Modal Content */
.modal-content {
    background: white;
    border-radius: 12px;
    max-width: 600px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    animation: slideUp 0.3s;
}

.modal-content.modal-large {
    max-width: 900px;
}

@keyframes slideUp {
    from {
        transform: translateY(20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
    margin: 0;
    color: #2c3e50;
    font-size: 1.25rem;
}

.btn-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #7f8c8d;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-close:hover {
    background: #f8f9fa;
    color: #2c3e50;
}

.modal-body {
    padding: 1.5rem;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid #e9ecef;
}

/* Booking Details Modal */
.details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.details-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.details-section.full-width {
    grid-column: 1 / -1;
}

.details-section h4 {
    margin: 0 0 0.5rem 0;
    color: #2c3e50;
    font-size: 1rem;
    font-weight: 600;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e9ecef;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f8f9fa;
}

.detail-row:last-child {
    border-bottom: none;
}

.detail-row .label {
    font-weight: 500;
    color: #7f8c8d;
    font-size: 0.9rem;
    min-width: 140px;
}

.detail-row .value {
    color: #2c3e50;
    text-align: right;
    flex: 1;
    font-size: 0.9rem;
}

.detail-row .value.total {
    font-weight: 700;
    font-size: 1.1rem;
    color: #27ae60;
}

.discount-text {
    color: #e74c3c !important;
    font-weight: 600;
}

/* Booking Form */
.booking-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

.form-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-group label {
    font-weight: 600;
    color: #2c3e50;
    font-size: 0.9rem;
}

.form-group input,
.form-group select,
.form-group textarea {
    padding: 0.875rem 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.2s;
    font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea {
    resize: vertical;
    min-height: 80px;
}

/* Warning Text */
.warning-text {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1rem;
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 8px;
    color: #856404;
    margin-bottom: 1rem;
    line-height: 1.5;
}

/* Responsive Design */
@media (max-width: 1400px) {
    .bookings-table {
        font-size: 0.85rem;
    }

    .bookings-table th,
    .bookings-table td {
        padding: 0.75rem;
    }
}

@media (max-width: 1200px) {
    .table-container {
        overflow-x: auto;
    }

    .bookings-table {
        min-width: 1000px;
    }
}

@media (max-width: 768px) {
    .bookings-page {
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

    .stats-overview {
        grid-template-columns: repeat(2, 1fr);
    }

    .filter-group {
        grid-template-columns: 1fr;
    }

    .details-grid {
        grid-template-columns: 1fr;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .pagination {
        flex-direction: column;
        gap: 1rem;
    }

    .page-numbers {
        flex-wrap: wrap;
        justify-content: center;
    }

    .modal-content {
        margin: 1rem;
    }
}

@media (max-width: 480px) {
    .header-content h1 {
        font-size: 1.5rem;
    }

    .stats-overview {
        grid-template-columns: 1fr;
    }

    .stat-card {
        padding: 1rem;
    }

    .stat-icon {
        width: 40px;
        height: 40px;
        font-size: 1.25rem;
    }

    .stat-content h3 {
        font-size: 1.5rem;
    }

    .btn-action {
        width: 28px;
        height: 28px;
        font-size: 0.9rem;
    }
}

/* Print Styles */
@media print {

    .page-header,
    .filters-section,
    .pagination,
    .action-buttons {
        display: none;
    }

    .bookings-page {
        padding: 0;
        background: white;
    }

    .table-container {
        box-shadow: none;
    }
}

/* Dark Mode Support (Optional) */
@media (prefers-color-scheme: dark) {
    /* Add dark mode styles if needed */
}
</style>