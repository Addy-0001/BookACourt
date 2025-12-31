<template>
    <div class="bookings-page">
        <!-- Page Header -->
        <div class="page-header">
            <div class="header-content">
                <h1>📅 Bookings Management</h1>
                <p class="subtitle">View and manage bookings for your courts</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-primary" @click="showCreateModal = true">
                    <span class="icon">➕</span>
                    <span>New Booking</span>
                </button>
                <button class="btn btn-secondary" @click="refreshBookings">
                    <span class="icon">🔄</span>
                    <span>Refresh</span>
                </button>
            </div>
        </div>

        <!-- Your Futsals Section -->
        <section class="futsals-section">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="icon">🏟️</span>
                    <span>Your Futsals</span>
                </h2>
                <router-link to="/admin/courts/create" class="btn btn-success btn-add-new">
                    <span class="icon">⊕</span>
                    <span>Add New</span>
                </router-link>
            </div>

            <!-- Loading State -->
            <div v-if="courtsLoading" class="loading-container">
                <div class="spinner"></div>
                <p>Loading your courts...</p>
            </div>

            <!-- Courts Grid -->
            <div v-else-if="adminStore.courts.length > 0" class="futsals-grid">
                <div v-for="court in adminStore.courts" :key="court.id"
                    :class="['futsal-card', { selected: selectedCourt?.id === court.id }]" @click="selectCourt(court)">
                    <!-- Court Image -->
                    <div class="futsal-image">
                        <img v-if="court.primary_image" :src="court.primary_image" :alt="court.name" />
                        <div v-else class="futsal-placeholder">
                            <span class="placeholder-icon">🏟️</span>
                        </div>
                        <span :class="['status-badge', court.is_active ? 'active' : 'inactive']">
                            {{ court.is_active ? 'Active' : 'Inactive' }}
                        </span>
                    </div>

                    <!-- Court Info -->
                    <div class="futsal-info">
                        <h3 class="futsal-name">{{ court.name }}</h3>
                        <p class="futsal-description">{{ court.description || 'Futsal court for bookings' }}</p>

                        <div class="futsal-details">
                            <div class="detail-item">
                                <span class="detail-icon">📍</span>
                                <span>{{ court.city }}</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-icon">📅</span>
                                <span>{{ formatDate(court.created_at) }}</span>
                            </div>
                        </div>

                        <p class="futsal-id">ID: {{ court.id }}</p>

                        <div class="futsal-actions">
                            <router-link :to="`/admin/courts/${court.id}/settings`" class="btn-action admin"
                                @click.stop>
                                <span class="icon">📊</span>
                                <span>Admin</span>
                            </router-link>
                            <button class="btn-action bookings" @click.stop="selectCourt(court)">
                                <span class="icon">📅</span>
                                <span>Regular Bookings</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="empty-state">
                <div class="empty-icon">🏟️</div>
                <h3>No Courts Found</h3>
                <p>Add your first court to start receiving bookings.</p>
                <router-link to="/admin/courts/create" class="btn btn-primary" style="margin-top: 1rem;">
                    <span>➕</span>
                    <span>Add Your First Court</span>
                </router-link>
            </div>
        </section>

        <!-- Recent Bookings Section -->
        <section v-if="selectedCourt" class="bookings-section">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="icon">📅</span>
                    <span>{{ selectedCourt.name }} Statistics</span>
                </h2>
                <router-link to="/admin/bookings" class="view-all-link">
                    View All →
                </router-link>
            </div>

            <!-- Date Selector -->
            <div class="date-selector">
                <label>Select Date:</label>
                <input v-model="selectedDate" type="date" class="date-input" @change="loadBookingsForDate" />
            </div>

            <!-- Bookings Info -->
            <div class="bookings-info">
                <h3 class="bookings-title">
                    Bookings for {{ formatBookingDate(selectedDate) }}:
                </h3>
            </div>

            <!-- Loading Bookings -->
            <div v-if="bookingsLoading" class="loading-container">
                <div class="spinner"></div>
                <p>Loading bookings...</p>
            </div>

            <!-- Time Slots Grid -->
            <div v-else class="time-slots-grid">
                <div v-for="slot in timeSlots" :key="slot.time" :class="['time-slot', getSlotClass(slot)]">
                    <span class="slot-time">{{ slot.time }}</span>
                    <div v-if="slot.booking" class="slot-booking-info">
                        <p class="booking-player">{{ slot.booking.player_name }}</p>
                        <p class="booking-status">{{ slot.booking.status }}</p>
                    </div>
                </div>
            </div>

            <!-- Booking Legend -->
            <div class="booking-legend">
                <div class="legend-item">
                    <span class="legend-color available"></span>
                    <span>Available</span>
                </div>
                <div class="legend-item">
                    <span class="legend-color booked"></span>
                    <span>Booked</span>
                </div>
                <div class="legend-item">
                    <span class="legend-color blocked"></span>
                    <span>Blocked</span>
                </div>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAdminStore } from '@/stores/admin';

const router = useRouter();
const adminStore = useAdminStore();

// State
const courtsLoading = ref(false);
const bookingsLoading = ref(false);
const selectedCourt = ref(null);
const selectedDate = ref(getTodayDate());
const showCreateModal = ref(false);
const courtBookings = ref([]);

// Time slots from 6 AM to 10 PM
const allTimeSlots = [
    '6-7', '7-8', '8-9', '9-10', '10-11', '11-12',
    '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
    '18-19', '19-20', '20-21', '21-22'
];

// Computed
const timeSlots = computed(() => {
    return allTimeSlots.map(time => {
        const [startHour, endHour] = time.split('-').map(Number);
        const booking = courtBookings.value.find(b => {
            const bookingStartHour = parseInt(b.start_time.split(':')[0]);
            return bookingStartHour === startHour;
        });

        return {
            time,
            startHour,
            endHour,
            booking,
            isBooked: !!booking,
            isBlocked: false // You can add blocked slots logic here
        };
    });
});

// Lifecycle
onMounted(async () => {
    await loadCourts();
});

// Watch for court selection
watch(selectedCourt, async (newCourt) => {
    if (newCourt) {
        await loadBookingsForDate();
    }
});

// Methods
async function loadCourts() {
    courtsLoading.value = true;
    try {
        await adminStore.fetchMyCourts();

        // Auto-select first court if none selected
        if (adminStore.courts.length > 0 && !selectedCourt.value) {
            selectedCourt.value = adminStore.courts[0];
            await loadBookingsForDate();
        }
    } catch (error) {
        console.error('Error loading courts:', error);
    } finally {
        courtsLoading.value = false;
    }
}

function selectCourt(court) {
    selectedCourt.value = court;
}

async function loadBookingsForDate() {
    if (!selectedCourt.value) return;

    bookingsLoading.value = true;
    try {
        await adminStore.fetchMyBookings({
            court: selectedCourt.value.id,
            booking_date: selectedDate.value,
        });

        // Filter bookings for the selected court and date
        courtBookings.value = adminStore.bookings.filter(
            b => b.court === selectedCourt.value.id && b.booking_date === selectedDate.value
        );
    } catch (error) {
        console.error('Error loading bookings:', error);
    } finally {
        bookingsLoading.value = false;
    }
}

async function refreshBookings() {
    await loadCourts();
    if (selectedCourt.value) {
        await loadBookingsForDate();
    }
}

function getSlotClass(slot) {
    if (slot.isBlocked) return 'blocked';
    if (slot.isBooked) return 'booked';
    return 'available';
}

function getTodayDate() {
    return new Date().toISOString().split('T')[0];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'numeric',
        day: 'numeric',
        year: 'numeric',
    });
}

function formatBookingDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric',
    });
}
</script>

<style scoped>
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
    text-decoration: none;
    color: inherit;
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

.btn-success {
    background: #52A055;
    color: white;
}

.btn-success:hover {
    background: #46894a;
    transform: translateY(-2px);
}

.icon {
    font-size: 1.1rem;
}

/* Futsals Section */
.futsals-section {
    margin-bottom: 3rem;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.5rem;
    color: #52A055;
    margin: 0;
    font-weight: 600;
}

.btn-add-new {
    padding: 0.625rem 1.25rem;
    font-size: 0.9rem;
}

/* Futsals Grid */
.futsals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
}

.futsal-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s;
    border: 3px solid transparent;
}

.futsal-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.futsal-card.selected {
    border-color: #52A055;
    box-shadow: 0 4px 16px rgba(82, 160, 85, 0.3);
}

/* Court Image */
.futsal-image {
    position: relative;
    width: 100%;
    height: 200px;
    overflow: hidden;
}

.futsal-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.futsal-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #52A055 0%, #46894a 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}

.placeholder-icon {
    font-size: 4rem;
    color: white;
}

.status-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: 0.375rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: capitalize;
    backdrop-filter: blur(10px);
}

.status-badge.active {
    background: rgba(39, 174, 96, 0.9);
    color: white;
}

.status-badge.inactive {
    background: rgba(149, 165, 166, 0.9);
    color: white;
}

/* Futsal Info */
.futsal-info {
    padding: 1.5rem;
}

.futsal-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: #52A055;
    margin: 0 0 0.5rem 0;
}

.futsal-description {
    font-size: 0.9rem;
    color: #7f8c8d;
    margin: 0 0 1rem 0;
    line-height: 1.4;
}

.futsal-details {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.detail-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: #2c3e50;
}

.detail-icon {
    font-size: 1rem;
}

.futsal-id {
    font-size: 0.8rem;
    color: #95a5a6;
    font-family: 'Courier New', monospace;
    margin: 0 0 1rem 0;
}

/* Futsal Actions */
.futsal-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
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

.btn-action.admin {
    background: #FFE8CC;
    color: #E67E22;
}

.btn-action.admin:hover {
    background: #E67E22;
    color: white;
}

.btn-action.bookings {
    background: #D6EAF8;
    color: #2980B9;
}

.btn-action.bookings:hover {
    background: #2980B9;
    color: white;
}

/* Bookings Section */
.bookings-section {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.view-all-link {
    color: #52A055;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s;
}

.view-all-link:hover {
    color: #46894a;
    text-decoration: underline;
}

/* Date Selector */
.date-selector {
    margin-bottom: 2rem;
}

.date-selector label {
    display: block;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.date-input {
    padding: 0.75rem 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    width: 300px;
    max-width: 100%;
    transition: all 0.2s;
}

.date-input:focus {
    outline: none;
    border-color: #52A055;
    box-shadow: 0 0 0 3px rgba(82, 160, 85, 0.1);
}

/* Bookings Info */
.bookings-info {
    margin-bottom: 2rem;
}

.bookings-title {
    font-size: 1.1rem;
    color: #2c3e50;
    font-weight: 600;
    margin: 0;
}

/* Time Slots Grid */
.time-slots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.time-slot {
    padding: 1.25rem 1rem;
    border-radius: 8px;
    text-align: center;
    transition: all 0.2s;
    border: 2px solid transparent;
}

.time-slot.available {
    background: #D5F4E6;
    color: #52A055;
    cursor: pointer;
}

.time-slot.available:hover {
    background: #B8EDD5;
    border-color: #52A055;
}

.time-slot.booked {
    background: #E8F5E9;
    color: #52A055;
    border: 2px solid #52A055;
}

.time-slot.blocked {
    background: #E0E0E0;
    color: #7f8c8d;
    cursor: not-allowed;
}

.slot-time {
    display: block;
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.slot-booking-info {
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid rgba(82, 160, 85, 0.3);
}

.booking-player {
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0 0 0.25rem 0;
}

.booking-status {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0;
    opacity: 0.8;
}

/* Booking Legend */
.booking-legend {
    display: flex;
    gap: 2rem;
    justify-content: center;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: #2c3e50;
}

.legend-color {
    width: 20px;
    height: 20px;
    border-radius: 4px;
}

.legend-color.available {
    background: #D5F4E6;
    border: 2px solid #52A055;
}

.legend-color.booked {
    background: #E8F5E9;
    border: 2px solid #52A055;
}

.legend-color.blocked {
    background: #E0E0E0;
    border: 2px solid #7f8c8d;
}

/* Loading & Empty States */
.loading-container,
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 2rem;
    text-align: center;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #52A055;
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
    margin: 0;
}

/* Responsive */
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

    .futsals-grid {
        grid-template-columns: 1fr;
    }

    .time-slots-grid {
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    }

    .date-input {
        width: 100%;
    }

    .booking-legend {
        flex-direction: column;
        gap: 1rem;
    }
}
</style>