<template>
  <div class="admin-homepage">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <h1>Admin Dashboard</h1>
        <p class="subtitle">Welcome back, {{ currentUser?.full_name || 'Admin' }}</p>
      </div>
      <div class="header-actions">
        <button class="btn-refresh" @click="refreshDashboard" :disabled="loading">
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
      <button class="btn-retry" @click="refreshDashboard">Try Again</button>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Statistics Overview -->
      <section class="stats-section">
        <h2 class="section-title">Overview</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-icon users">👥</span>
              <span class="stat-label">Total Users</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ dashboardStats.totalUsers }}</h3>
              <p class="stat-change positive">+12% from last month</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-icon courts">🏟️</span>
              <span class="stat-label">Active Courts</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ dashboardStats.totalCourts }}</h3>
              <p class="stat-change positive">+5% from last month</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-header">
              <span class="stat-icon bookings">📅</span>
              <span class="stat-label">Total Bookings</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ dashboardStats.totalBookings }}</h3>
              <p class="stat-change positive">+18% from last month</p>
            </div>
          </div>

          <div class="stat-card highlight">
            <div class="stat-header">
              <span class="stat-icon pending">⏳</span>
              <span class="stat-label">Pending Approvals</span>
            </div>
            <div class="stat-body">
              <h3 class="stat-number">{{ dashboardStats.pendingRegistrations }}</h3>
              <p class="stat-description">Requires attention</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Quick Actions Grid -->
      <section class="quick-actions-section">
        <h2 class="section-title">Quick Actions</h2>
        <div class="actions-grid">
          <router-link to="/admin/users" class="action-card">
            <div class="action-icon">👥</div>
            <h3>Manage Users</h3>
            <p>View and manage all users</p>
          </router-link>

          <router-link to="/admin/courts" class="action-card">
            <div class="action-icon">🏟️</div>
            <h3>Manage Courts</h3>
            <p>View and manage courts</p>
          </router-link>

          <router-link to="/admin/bookings" class="action-card">
            <div class="action-icon">📅</div>
            <h3>Manage Bookings</h3>
            <p>View all bookings</p>
          </router-link>

          <router-link to="/admin/registrations" class="action-card">
            <div class="action-icon">📝</div>
            <h3>Review Registrations</h3>
            <p>Approve or reject court registrations</p>
            <span v-if="dashboardStats.pendingRegistrations > 0" class="badge">
              {{ dashboardStats.pendingRegistrations }}
            </span>
          </router-link>

          <router-link to="/admin/categories" class="action-card">
            <div class="action-icon">📂</div>
            <h3>Manage Categories</h3>
            <p>Court categories</p>
          </router-link>

          <router-link to="/admin/reports" class="action-card">
            <div class="action-icon">📊</div>
            <h3>View Reports</h3>
            <p>Analytics and insights</p>
          </router-link>
        </div>
      </section>

      <!-- Two Column Layout: Pending Items + Recent Activity -->
      <div class="two-column-section">
        <!-- Pending Registrations -->
        <section class="pending-section">
          <div class="section-header">
            <h2 class="section-title">Pending Registrations</h2>
            <router-link to="/admin/registrations" class="link-view-all">
              View All
            </router-link>
          </div>

          <div v-if="pendingRegistrations.length === 0" class="empty-state">
            <p>✅ No pending registrations</p>
          </div>

          <div v-else class="registration-list">
            <div v-for="registration in pendingRegistrations.slice(0, 5)" :key="registration.id"
              class="registration-item">
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
                <button class="btn-icon btn-approve" @click="handleApprove(registration.id)" :disabled="processing"
                  title="Approve">
                  ✓
                </button>
                <button class="btn-icon btn-reject" @click="handleReject(registration.id)" :disabled="processing"
                  title="Reject">
                  ✕
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Recent Activity -->
        <section class="activity-section">
          <div class="section-header">
            <h2 class="section-title">Recent Activity</h2>
            <router-link to="/admin/bookings" class="link-view-all">
              View All
            </router-link>
          </div>

          <div v-if="recentBookings.length === 0" class="empty-state">
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
                  {{ booking.player_name }} • {{ formatDate(booking.booking_date) }}
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

      <!-- Charts Section (Placeholder) -->
      <section class="charts-section">
        <div class="chart-card">
          <h3>Bookings Overview</h3>
          <div class="chart-placeholder">
            <p>📈 Chart will be implemented here</p>
            <p class="chart-note">Monthly booking trends</p>
          </div>
        </div>

        <div class="chart-card">
          <h3>Revenue Analytics</h3>
          <div class="chart-placeholder">
            <p>💰 Chart will be implemented here</p>
            <p class="chart-note">Revenue by month</p>
          </div>
        </div>
      </section>
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
          <textarea id="reject-reason" v-model="rejectReason" placeholder="Please provide a reason..."
            rows="4"></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeRejectModal">Cancel</button>
          <button class="btn-danger" @click="confirmReject" :disabled="!rejectReason.trim() || processing">
            Confirm Rejection
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAdminStore } from '@/stores/admin';

const adminStore = useAdminStore();

// State
const loading = ref(true);
const error = ref(null);
const processing = ref(false);
const showRejectModal = ref(false);
const rejectReason = ref('');
const selectedRegistrationId = ref(null);

// Computed
const currentUser = computed(() => {
  // Get from auth store or localStorage
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
});

const dashboardStats = computed(() => adminStore.dashboardStats);
const pendingRegistrations = computed(() => adminStore.pendingRegistrations);
const recentBookings = computed(() => adminStore.bookings.slice(0, 5));

// Lifecycle
onMounted(async () => {
  await loadDashboard();
});

// Methods
async function loadDashboard() {
  loading.value = true;
  error.value = null;

  try {
    await Promise.all([
      adminStore.fetchDashboardStats(),
      adminStore.fetchRegistrations({ status: 'PENDING' }),
      adminStore.fetchBookings({ ordering: '-created_at', page_size: 5 }),
    ]);
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

async function handleApprove(registrationId) {
  if (!confirm('Are you sure you want to approve this registration?')) return;

  processing.value = true;
  try {
    await adminStore.approveRegistration(registrationId);
    alert('✅ Registration approved successfully!');
  } catch (err) {
    alert('❌ Failed to approve registration');
    console.error('Approve error:', err);
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
    await adminStore.rejectRegistration(
      selectedRegistrationId.value,
      rejectReason.value
    );
    alert('✅ Registration rejected');
    closeRejectModal();
  } catch (err) {
    alert('❌ Failed to reject registration');
    console.error('Reject error:', err);
  } finally {
    processing.value = false;
  }
}

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

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover:not(:disabled) {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Loading State */
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
  border-top: 4px solid #3498db;
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

.btn-retry {
  margin-top: 1rem;
  padding: 0.75rem 2rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

/* Section Styling */
.section-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.link-view-all {
  color: #3498db;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.link-view-all:hover {
  color: #2980b9;
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
}

.stat-change.positive {
  color: #27ae60;
}

/* Quick Actions */
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

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #95a5a6;
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
}

.btn-reject {
  background: #f8d7da;
  color: #721c24;
}

.btn-reject:hover:not(:disabled) {
  background: #e74c3c;
  color: white;
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
}

.activity-icon {
  font-size: 1.5rem;
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

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
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

/* Charts Section */
.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.chart-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  color: #7f8c8d;
}

.chart-placeholder p {
  margin: 0.5rem 0;
}

.chart-note {
  font-size: 0.85rem;
  color: #95a5a6;
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
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
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
}

.btn-close:hover {
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
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  resize: vertical;
}

.modal-body textarea:focus {
  outline: none;
  border-color: #3498db;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.btn-secondary,
.btn-danger {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-secondary {
  background: #e9ecef;
  color: #495057;
}

.btn-secondary:hover {
  background: #dee2e6;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .admin-homepage {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .stats-grid,
  .actions-grid,
  .two-column-section,
  .charts-section {
    grid-template-columns: 1fr;
  }

  .stat-number {
    font-size: 2rem;
  }

  .action-card {
    padding: 1.5rem;
  }
}
</style>