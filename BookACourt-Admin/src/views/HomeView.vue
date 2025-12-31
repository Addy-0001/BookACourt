<template>
  <div class="admin-homepage">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>{{ dashboardTitle }}</h1>
        <p class="subtitle">{{ greetingMessage }}</p>
      </div>
      <div class="header-actions">
        <button v-if="isCourtOwnerOrManager" class="btn btn-primary" @click="navigateToCreateCourt">
          <span class="icon">➕</span>
          <span>Add New Court</span>
        </button>
        <button class="btn btn-secondary" @click="refreshDashboard" :disabled="loading">
          <span class="icon">🔄</span>
          <span>Refresh</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <h3>Failed to Load Dashboard</h3>
      <p>{{ error }}</p>
      <button class="btn btn-primary" @click="refreshDashboard">Try Again</button>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Statistics Overview -->
      <section class="stats-section">
        <h2 class="section-title">Overview</h2>
        <div class="stats-grid">
          <!-- Super User Stats -->
          <div class="stat-card" v-if="isSuperUser">
            <div class="stat-header">
              <span class="stat-icon">👥</span>
              <span class="stat-label">Total Users</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ formatNumber(adminStore.dashboardStats.totalUsers) }}</h3>
              <p class="stat-change positive">
                <span>Platform wide</span>
              </p>
            </div>
          </div>

          <!-- My Courts -->
          <div class="stat-card highlight">
            <div class="stat-header">
              <span class="stat-icon">🏟️</span>
              <span class="stat-label">{{ isCourtOwnerOrManager ? 'My Courts' : 'Total Courts' }}</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ adminStore.courts.length }}</h3>
              <p class="stat-change" :class="courtStats.activePercentage >= 80 ? 'positive' : 'neutral'">
                <span>{{ courtStats.active }} active</span>
              </p>
            </div>
          </div>

          <!-- Total Bookings -->
          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-icon">📅</span>
              <span class="stat-label">Total Bookings</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ formatNumber(adminStore.bookings.length) }}</h3>
              <p class="stat-change positive">
                <span>{{ adminStore.todayBookings.length }} today</span>
              </p>
            </div>
          </div>

          <!-- Pending Approvals (Super User) -->
          <div class="stat-card highlight" v-if="isSuperUser">
            <div class="stat-header">
              <span class="stat-icon">⏳</span>
              <span class="stat-label">Pending Approvals</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ adminStore.dashboardStats.pendingRegistrations }}</h3>
              <p class="stat-description">Requires attention</p>
            </div>
          </div>

          <!-- Week Revenue -->
          <div class="stat-card" v-if="isCourtOwnerOrManager">
            <div class="stat-header">
              <span class="stat-icon">💰</span>
              <span class="stat-label">This Week</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">NPR {{ formatCurrency(adminStore.weekRevenue) }}</h3>
              <p class="stat-change positive">
                <span>Revenue</span>
              </p>
            </div>
          </div>

          <!-- Month Revenue -->
          <div class="stat-card" v-if="isCourtOwnerOrManager">
            <div class="stat-header">
              <span class="stat-icon">📊</span>
              <span class="stat-label">This Month</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">NPR {{ formatCurrency(adminStore.monthRevenue) }}</h3>
              <p class="stat-change positive">
                <span>Revenue</span>
              </p>
            </div>
          </div>

          <!-- Occupancy Rate -->
          <div class="stat-card" v-if="isCourtOwnerOrManager">
            <div class="stat-header">
              <span class="stat-icon">📈</span>
              <span class="stat-label">Occupancy Rate</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ adminStore.dashboardStats.occupancyRate }}%</h3>
              <p class="stat-change" :class="adminStore.dashboardStats.occupancyRate >= 70 ? 'positive' : 'neutral'">
                <span>Average</span>
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Quick Actions for All Users -->
      <section class="quick-actions-section" v-if="quickActions.length > 0">
        <h2 class="section-title">Quick Actions</h2>
        <div class="actions-grid">
          <component
            v-for="action in quickActions"
            :key="action.route"
            :is="action.route ? 'router-link' : 'button'"
            :to="action.route"
            @click="action.onClick"
            class="action-card"
          >
            <div class="action-icon">{{ action.icon }}</div>
            <h3>{{ action.title }}</h3>
            <p>{{ action.description }}</p>
            <span v-if="action.badge" class="badge">{{ action.badge }}</span>
          </component>
        </div>
      </section>

      <!-- My Courts Section (For Court Owners/Managers) -->
      <section v-if="isCourtOwnerOrManager" class="courts-section">
        <div class="section-header">
          <h2 class="section-title">My Courts</h2>
          <div class="section-actions">
            <div class="filter-tabs">
              <button
                v-for="filter in courtFilters"
                :key="filter.value"
                :class="['tab', { active: activeCourtFilter === filter.value }]"
                @click="activeCourtFilter = filter.value"
              >
                {{ filter.label }}
                <span v-if="filter.count > 0" class="tab-badge">{{ filter.count }}</span>
              </button>
            </div>
            <router-link to="/admin/my-courts" class="link-view-all">
              View All Courts →
            </router-link>
          </div>
        </div>

        <!-- Courts Grid -->
        <div v-if="displayedCourts.length > 0" class="courts-grid">
          <div v-for="court in displayedCourts" :key="court.id" class="court-card">
            <div class="court-image">
              <img v-if="court.primary_image" :src="court.primary_image" :alt="court.name" />
              <span v-else class="court-placeholder">🏟️</span>
              <span :class="['court-status-badge', court.is_active ? 'status-active' : 'status-inactive']">
                {{ court.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
            
            <div class="court-content">
              <div class="court-header">
                <div>
                  <h3 class="court-title">{{ court.name }}</h3>
                  <p class="court-location">
                    <span>📍</span>
                    <span>{{ court.city }}</span>
                  </p>
                </div>
              </div>

              <div class="court-details">
                <div class="detail-item">
                  <span>🏀</span>
                  <span>{{ court.court_type }}</span>
                </div>
                <div class="detail-item">
                  <span>{{ court.is_indoor ? '🏠' : '☀️' }}</span>
                  <span>{{ court.is_indoor ? 'Indoor' : 'Outdoor' }}</span>
                </div>
                <div class="detail-item">
                  <span>💰</span>
                  <span>NPR {{ court.base_hourly_rate }}/hr</span>
                </div>
                <div class="detail-item">
                  <span>⭐</span>
                  <span>{{ court.average_rating || 'N/A' }} ({{ court.total_reviews || 0 }})</span>
                </div>
              </div>

              <div class="court-stats">
                <div class="stat-item">
                  <span class="stat-value">{{ getCourtBookingCount(court.id, 'today') }}</span>
                  <span class="stat-text">Today</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ getCourtBookingCount(court.id, 'week') }}</span>
                  <span class="stat-text">This Week</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ getCourtOccupancy(court.id) }}%</span>
                  <span class="stat-text">Occupancy</span>
                </div>
              </div>

              <div class="court-actions">
                <router-link :to="`/admin/courts/${court.id}`" class="btn-action btn-view">
                  <span>👁️</span>
                  <span>View</span>
                </router-link>
                <router-link :to="`/admin/courts/${court.id}/edit`" class="btn-action btn-edit">
                  <span>✏️</span>
                  <span>Edit</span>
                </router-link>
                <router-link :to="`/admin/courts/${court.id}/settings`" class="btn-action btn-settings">
                  <span>⚙️</span>
                  <span>Settings</span>
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">🏟️</div>
          <h3>No Courts Found</h3>
          <p>{{ getEmptyStateMessage() }}</p>
          <button class="btn btn-primary" @click="navigateToCreateCourt" style="margin-top: 1rem;">
            <span>➕</span>
            <span>Add Your First Court</span>
          </button>
        </div>
      </section>

      <!-- Two Column Layout -->
      <div class="two-column-section">
        <!-- Pending Items (Super User) -->
        <section v-if="isSuperUser && adminStore.pendingRegistrations.length > 0" class="pending-section">
          <div class="section-header">
            <h2 class="section-title">Pending Registrations</h2>
            <router-link to="/admin/registrations" class="link-view-all">
              View All
            </router-link>
          </div>

          <div class="registration-list">
            <div
              v-for="registration in adminStore.pendingRegistrations.slice(0, 5)"
              :key="registration.id"
              class="registration-item"
            >
              <div class="registration-info">
                <h4>{{ registration.court_name }}</h4>
                <p class="registration-meta">
                  <span>{{ registration.owner_name }}</span>
                  <span class="separator">•</span>
                  <span>{{ registration.city }}</span>
                </p>
                <p class="registration-date">
                  {{ formatDate(registration.created_at) }}
                </p>
              </div>
              <div class="registration-actions">
                <button
                  class="btn-icon btn-approve"
                  @click="handleApprove(registration.id)"
                  :disabled="processing"
                  title="Approve"
                >
                  ✓
                </button>
                <button
                  class="btn-icon btn-reject"
                  @click="handleReject(registration.id)"
                  :disabled="processing"
                  title="Reject"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Recent Bookings -->
        <section class="activity-section">
          <div class="section-header">
            <h2 class="section-title">Recent Bookings</h2>
            <router-link to="/admin/bookings" class="link-view-all">
              View All
            </router-link>
          </div>

          <div v-if="recentBookings.length === 0" class="empty-state-small">
            <p>No recent bookings</p>
          </div>

          <div v-else class="activity-list">
            <div v-for="booking in recentBookings" :key="booking.id" class="activity-item">
              <div class="activity-icon">
                <span>📅</span>
              </div>
              <div class="activity-info">
                <h4>{{ booking.court_name }}</h4>
                <p class="activity-meta">
                  {{ booking.player_name }} • {{ formatDate(booking.booking_date) }} • {{ formatTime(booking.start_time) }}
                </p>
              </div>
              <div class="activity-status">
                <span :class="['status-badge', getStatusClass(booking.status)]">
                  {{ booking.status }}
                </span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- Rejection Modal -->
    <div v-if="showRejectModal" class="modal-overlay" @click="closeRejectModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Reject Registration</h3>
          <button class="btn-close" @click="closeRejectModal">✕</button>
        </div>
        <div class="modal-body">
          <label for="reject-reason">Reason for rejection:</label>
          <textarea
            id="reject-reason"
            v-model="rejectReason"
            placeholder="Please provide a reason..."
            rows="4"
          ></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeRejectModal">Cancel</button>
          <button
            class="btn-danger"
            @click="confirmReject"
            :disabled="!rejectReason.trim() || processing"
          >
            Confirm Rejection
          </button>
        </div>
      </div>
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
const loading = ref(true);
const error = ref(null);
const processing = ref(false);
const showRejectModal = ref(false);
const rejectReason = ref('');
const selectedRegistrationId = ref(null);
const activeCourtFilter = ref('all');

// Computed
const currentUser = computed(() => adminStore.currentUser);
const isSuperUser = computed(() => adminStore.isSuperUser);
const isCourtOwner = computed(() => adminStore.isCourtOwner);
const isCourtManager = computed(() => adminStore.isCourtManager);
const isCourtOwnerOrManager = computed(() => adminStore.isCourtOwnerOrManager);

const dashboardTitle = computed(() => {
  if (isSuperUser.value) return 'Admin Dashboard';
  if (isCourtOwner.value) return 'Court Owner Dashboard';
  if (isCourtManager.value) return 'Court Manager Dashboard';
  return 'Dashboard';
});

const greetingMessage = computed(() => {
  const hour = new Date().getHours();
  let greeting = 'Good morning';
  if (hour >= 12 && hour < 17) greeting = 'Good afternoon';
  else if (hour >= 17) greeting = 'Good evening';
  
  return `${greeting}, ${currentUser.value?.full_name || 'Admin'}! Welcome back.`;
});

const courtStats = computed(() => {
  const total = adminStore.courts.length;
  const active = adminStore.activeCourts.length;
  const activePercentage = total > 0 ? Math.round((active / total) * 100) : 0;
  return { total, active, activePercentage };
});

const courtFilters = computed(() => [
  { label: 'All Courts', value: 'all', count: adminStore.courts.length },
  { label: 'Active', value: 'active', count: adminStore.activeCourts.length },
  { label: 'Inactive', value: 'inactive', count: adminStore.inactiveCourts.length },
]);

const displayedCourts = computed(() => {
  let courts = adminStore.courts;
  
  if (activeCourtFilter.value === 'active') {
    courts = adminStore.activeCourts;
  } else if (activeCourtFilter.value === 'inactive') {
    courts = adminStore.inactiveCourts;
  }
  
  // Show only first 6 courts
  return courts.slice(0, 6);
});

const recentBookings = computed(() => adminStore.bookings.slice(0, 5));

const quickActions = computed(() => {
  const actions = [];
  
  if (isSuperUser.value) {
    actions.push(
      { route: '/admin/users', icon: '👥', title: 'Manage Users', description: 'View and manage all users' },
      { route: '/admin/courts', icon: '🏟️', title: 'All Courts', description: 'View and manage all courts' },
      { route: '/admin/registrations', icon: '📝', title: 'Review Registrations', description: 'Approve or reject court registrations', badge: adminStore.dashboardStats.pendingRegistrations || null },
      { route: '/admin/categories', icon: '📂', title: 'Manage Categories', description: 'Court categories' }
    );
  }
  
  if (isCourtOwnerOrManager.value) {
    actions.push(
      { route: '/admin/my-courts', icon: '🏟️', title: 'My Courts', description: 'Manage your courts' },
      { route: '/admin/bookings', icon: '📅', title: 'Bookings', description: 'View and manage bookings' },
      { route: '/admin/reviews', icon: '⭐', title: 'Reviews', description: 'View and respond to reviews' },
      { route: '/admin/equipment', icon: '🎾', title: 'Equipment', description: 'Manage court equipment' }
    );
  }
  
  // Common actions
  actions.push(
    { route: '/admin/reports', icon: '📊', title: 'Reports', description: 'Analytics and insights' }
  );
  
  return actions;
});

// Lifecycle
onMounted(async () => {
  await loadDashboard();
});

// Methods
async function loadDashboard() {
  loading.value = true;
  error.value = null;

  try {
    // Initialize admin store
    await adminStore.initialize();

    // Load user-specific data
    if (isSuperUser.value) {
      await adminStore.fetchRegistrations({ status: 'PENDING' });
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load dashboard data';
    console.error('Dashboard error:', err);
  } finally {
    loading.value = false;
  }
}

async function refreshDashboard() {
  await loadDashboard();
}

function navigateToCreateCourt() {
  router.push('/admin/my-courts/create');
}

function getCourtBookingCount(courtId, period) {
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

function getCourtOccupancy(courtId) {
  const courtBookings = adminStore.bookings.filter(
    b => b.court === courtId && (b.status === 'CONFIRMED' || b.status === 'COMPLETED')
  );
  // Simple calculation: assume 10 hours per day, 30 days
  const totalSlots = 10 * 30;
  const occupiedSlots = courtBookings.length;
  return Math.round((occupiedSlots / totalSlots) * 100);
}

async function handleApprove(registrationId) {
  if (!confirm('Are you sure you want to approve this registration?')) return;

  processing.value = true;
  try {
    await adminStore.approveRegistration(registrationId);
    alert('✅ Registration approved successfully!');
  } catch (err) {
    alert('❌ Failed to approve registration');
  } finally {
    processing.value = false;
  }
}

function handleReject(registrationId) {
  selectedRegistrationId.value = registrationId;
  showRejectModal.value = true;
  rejectReason.value = '';
}

function closeRejectModal() {
  showRejectModal.value = false;
  selectedRegistrationId.value = null;
  rejectReason.value = '';
}

async function confirmReject() {
  if (!rejectReason.value.trim()) return;

  processing.value = true;
  try {
    await adminStore.rejectRegistration(selectedRegistrationId.value, rejectReason.value);
    alert('✅ Registration rejected');
    closeRejectModal();
  } catch (err) {
    alert('❌ Failed to reject registration');
  } finally {
    processing.value = false;
  }
}

function getEmptyStateMessage() {
  if (activeCourtFilter.value === 'active') {
    return 'No active courts. Activate your courts to start receiving bookings.';
  }
  if (activeCourtFilter.value === 'inactive') {
    return 'No inactive courts found.';
  }
  return 'Start by adding your first court to begin receiving bookings.';
}

// Utility Functions
function formatDate(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
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

function formatNumber(num) {
  return new Intl.NumberFormat('en-US').format(num);
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
</script>

<style scoped>
/* Keep all existing styles from the original HomeView.vue */
/* This is just showing the structure - use the original styles */

.admin-homepage {
  padding: 2rem;
  background: #f5f6fa;
  min-height: 100vh;
}

/* Add new styles for enhanced features */
.section-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.court-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.court-placeholder {
  font-size: 4rem;
}

.court-status-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  backdrop-filter: blur(10px);
}

.admin-homepage {
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
}

.subtitle {
  color: #7f8c8d;
  font-size: 1rem;
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  font-size: 1.1rem;
}

/* Loading/Error States */
.loading-container,
.error-container {
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

.error-container {
  color: #e74c3c;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Section Styling */
.section-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.link-view-all {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.2s;
}

.link-view-all:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* Stats Grid */
.stats-section {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-card.highlight {
  border-left: 4px solid #f39c12;
}

.stat-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.stat-icon {
  font-size: 2rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #7f8c8d;
  font-weight: 500;
}

.stat-body {
  padding-left: 2.75rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.stat-change,
.stat-description {
  font-size: 0.85rem;
  color: #95a5a6;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-change.positive {
  color: #27ae60;
}

.stat-change.negative {
  color: #e74c3c;
}

.stat-change.neutral {
  color: #7f8c8d;
}

/* Courts Section */
.courts-section {
  margin-bottom: 2rem;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
}

.tab {
  padding: 0.5rem 1rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab:hover {
  border-color: #667eea;
}

.tab.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.tab-badge {
  background: rgba(0, 0, 0, 0.1);
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 600;
}

.tab.active .tab-badge {
  background: rgba(255, 255, 255, 0.2);
}

.courts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.court-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.court-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.court-image {
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  color: white;
}

.court-content {
  padding: 1.5rem;
}

.court-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.court-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.court-location {
  font-size: 0.9rem;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.court-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-inactive {
  background: #f8d7da;
  color: #721c24;
}

.court-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 1rem 0;
  border-top: 1px solid #e9ecef;
  border-bottom: 1px solid #e9ecef;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #2c3e50;
}

.court-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.stat-text {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.court-actions {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.5rem;
}

.btn-action {
  padding: 0.625rem 0.75rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 500;
}

.btn-view {
  background: #e3f2fd;
  color: #1976d2;
}

.btn-view:hover {
  background: #1976d2;
  color: white;
}

.btn-edit {
  background: #fff3cd;
  color: #856404;
}

.btn-edit:hover {
  background: #ffc107;
  color: white;
}

.btn-settings {
  background: #e8f5e9;
  color: #2e7d32;
}

.btn-settings:hover {
  background: #4caf50;
  color: white;
}

/* Empty States */
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
}

.empty-state p {
  color: #7f8c8d;
  margin: 0;
}

.empty-state-small {
  text-align: center;
  padding: 2rem;
  color: #95a5a6;
  background: #f8f9fa;
  border-radius: 8px;
}

/* Quick Actions (Super Users) */
.quick-actions-section {
  margin-bottom: 2rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.action-card {
  position: relative;
  background: white;
  padding: 2rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  font-size: 1.1rem;
  margin: 0 0 0.5rem 0;
}

.action-card p {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0;
}

.action-card:hover p {
  color: rgba(255, 255, 255, 0.9);
}

.badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #e74c3c;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
}

/* Two Column Layout */
.two-column-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.pending-section,
.activity-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Registration List */
.registration-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.registration-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: background 0.2s;
}

.registration-item:hover {
  background: #e9ecef;
}

.registration-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.registration-meta {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0 0 0.25rem 0;
}

.separator {
  margin: 0 0.5rem;
}

.registration-date {
  font-size: 0.85rem;
  color: #95a5a6;
  margin: 0;
}

.registration-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.2s;
}

.btn-approve {
  background: #d4edda;
  color: #155724;
}

.btn-approve:hover:not(:disabled) {
  background: #27ae60;
  color: white;
  transform: scale(1.1);
}

.btn-reject {
  background: #f8d7da;
  color: #721c24;
}

.btn-reject:hover:not(:disabled) {
  background: #e74c3c;
  color: white;
  transform: scale(1.1);
}

.btn-icon:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Activity List */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: background 0.2s;
}

.activity-item:hover {
  background: #e9ecef;
}

.activity-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.activity-info {
  flex: 1;
}

.activity-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 0.95rem;
  color: #2c3e50;
}

.activity-meta {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin: 0;
}

.activity-status {
  flex-shrink: 0;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
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

/* Modal */
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
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
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
}

.btn-close:hover {
  background: #f8f9fa;
  color: #2c3e50;
}

.modal-body {
  padding: 1.5rem;
}

.modal-body label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.modal-body textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  resize: vertical;
  transition: border-color 0.2s;
}

.modal-body textarea:focus {
  outline: none;
  border-color: #667eea;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.btn-danger {
  padding: 0.75rem 1.5rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
  transform: translateY(-2px);
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 1200px) {
  .courts-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .admin-homepage {
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

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .filter-tabs {
    flex-wrap: wrap;
  }

  .courts-grid {
    grid-template-columns: 1fr;
  }

  .court-actions {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .two-column-section {
    grid-template-columns: 1fr;
  }

  .stat-number {
    font-size: 2rem;
  }

  .court-details {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .header-content h1 {
    font-size: 1.5rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  .stat-number {
    font-size: 1.75rem;
  }

  .court-image {
    height: 150px;
    font-size: 3rem;
  }

  .modal-content {
    width: 95%;
  }
}
</style>