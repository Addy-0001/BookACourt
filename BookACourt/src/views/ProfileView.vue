<template>
    <div class="profile-container">
        <!-- Enhanced Header with Brand Colors -->
        <div class="profile-header">
            <div class="header-content">
                <button @click="$router.go(-1)" class="header-btn back-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="19" y1="12" x2="5" y2="12"></line>
                        <polyline points="12 19 5 12 12 5"></polyline>
                    </svg>
                    <span>Back</span>
                </button>
                <h1 class="header-title">My Profile</h1>
                <button @click="handleLogout" class="header-btn logout-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                        <polyline points="16 17 21 12 16 7"></polyline>
                        <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                    <span>Logout</span>
                </button>
            </div>
        </div>

        <div class="profile-content">
            <!-- Profile Picture Section with Modern Design -->
            <div class="profile-picture-section">
                <div class="avatar-container">
                    <div class="avatar-wrapper">
                        <img v-if="user.profile_picture" :src="user.profile_picture" alt="Profile" class="avatar" />
                        <div v-else class="avatar-placeholder">
                            {{ user.full_name?.charAt(0).toUpperCase() }}
                        </div>
                    </div>
                    <button @click="editMode = true" class="edit-avatar-btn" title="Edit profile picture">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                    </button>
                </div>
                <div class="user-info">
                    <h2>{{ user.full_name }}</h2>
                    <span class="role-badge" :class="roleClass">{{ roleDisplay }}</span>
                </div>
            </div>

            <!-- Stats Cards for Players -->
            <div v-if="user.role === 'PLAYER'" class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon bookings">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="16" y1="2" x2="16" y2="6"></line>
                            <line x1="8" y1="2" x2="8" y2="6"></line>
                            <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                    </div>
                    <div class="stat-content">
                        <h3>Total Bookings</h3>
                        <p class="stat-number">{{ stats.total_bookings || 0 }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon points">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polygon
                                points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2">
                            </polygon>
                        </svg>
                    </div>
                    <div class="stat-content">
                        <h3>Loyalty Points</h3>
                        <p class="stat-number">{{ user.loyalty_points || 0 }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon matches">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polygon points="10 8 16 12 10 16 10 8"></polygon>
                        </svg>
                    </div>
                    <div class="stat-content">
                        <h3>Matches Played</h3>
                        <p class="stat-number">{{ stats.total_matches_played || 0 }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon rating">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                    </div>
                    <div class="stat-content">
                        <h3>Rating</h3>
                        <p class="stat-number">{{ stats.sportsmanship_rating || '5.0' }}/5.0</p>
                    </div>
                </div>
            </div>

            <!-- Personal Information Section -->
            <div class="profile-section">
                <div class="section-header">
                    <h3>Personal Information</h3>
                    <button v-if="!editMode" @click="editMode = true" class="edit-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                        Edit
                    </button>
                </div>

                <div v-if="successMessage" class="alert alert-success">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    {{ successMessage }}
                </div>

                <div v-if="errorMessage" class="alert alert-error">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    {{ errorMessage }}
                </div>

                <form @submit.prevent="handleUpdateProfile" class="profile-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Full Name</label>
                            <div class="input-wrapper">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                    <circle cx="12" cy="7" r="4"></circle>
                                </svg>
                                <input v-model="profileForm.full_name" type="text" :disabled="!editMode" required />
                            </div>
                        </div>

                        <div class="form-group">
                            <label>Phone Number</label>
                            <div class="input-wrapper">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <path
                                        d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                                    </path>
                                </svg>
                                <input v-model="profileForm.phone_number" type="tel" disabled />
                            </div>
                            <small class="field-hint">Phone number cannot be changed</small>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>Email</label>
                            <div class="input-wrapper">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <path
                                        d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z">
                                    </path>
                                    <polyline points="22,6 12,13 2,6"></polyline>
                                </svg>
                                <input v-model="profileForm.email" type="email" :disabled="!editMode" />
                            </div>
                        </div>

                        <div class="form-group">
                            <label>Date of Birth</label>
                            <div class="input-wrapper">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                    <line x1="16" y1="2" x2="16" y2="6"></line>
                                    <line x1="8" y1="2" x2="8" y2="6"></line>
                                    <line x1="3" y1="10" x2="21" y2="10"></line>
                                </svg>
                                <input v-model="profileForm.date_of_birth" type="date" :disabled="!editMode" />
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>City</label>
                        <div class="input-wrapper">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            <input v-model="profileForm.city" type="text" :disabled="!editMode"
                                placeholder="Your city" />
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Address</label>
                        <div class="input-wrapper">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round">
                                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                                <polyline points="9 22 9 12 15 12 15 22"></polyline>
                            </svg>
                            <textarea v-model="profileForm.address" :disabled="!editMode" rows="3"
                                placeholder="Your full address"></textarea>
                        </div>
                    </div>

                    <div v-if="editMode" class="form-actions">
                        <button type="button" @click="cancelEdit" class="btn btn-secondary">
                            Cancel
                        </button>
                        <button type="submit" class="btn btn-primary" :disabled="loading">
                            <span v-if="loading">Saving...</span>
                            <span v-else>Save Changes</span>
                        </button>
                    </div>
                </form>
            </div>

            <!-- Account Status Section -->
            <div class="profile-section">
                <div class="section-header">
                    <h3>Account Status</h3>
                </div>

                <div class="status-grid">
                    <div class="status-item">
                        <div class="status-label">Account Created</div>
                        <div class="status-value">{{ formatDate(user.created_at) }}</div>
                    </div>
                    <div class="status-item">
                        <div class="status-label">Phone Verified</div>
                        <div class="status-value">
                            <span v-if="user.is_phone_verified" class="badge badge-success">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                Verified
                            </span>
                            <span v-else class="badge badge-warning">Not Verified</span>
                        </div>
                    </div>
                    <div class="status-item">
                        <div class="status-label">Account Status</div>
                        <div class="status-value">
                            <span v-if="user.is_active" class="badge badge-success">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                Active
                            </span>
                            <span v-else class="badge badge-error">Inactive</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/services/api';

const router = useRouter();
const authStore = useAuthStore();

const user = ref({ ...authStore.user });
const stats = ref({});
const editMode = ref(false);
const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const profileForm = ref({
    full_name: user.value.full_name || '',
    email: user.value.email || '',
    phone_number: user.value.phone_number || '',
    date_of_birth: user.value.date_of_birth || '',
    city: user.value.city || '',
    address: user.value.address || '',
});

const roleClass = computed(() => {
    const roleMap = {
        'PLAYER': 'role-player',
        'COURT_OWNER': 'role-owner',
        'COURT_MANAGER': 'role-manager',
        'SUPER_USER': 'role-admin'
    };
    return roleMap[user.value.role] || 'role-player';
});

const roleDisplay = computed(() => {
    const roleMap = {
        'PLAYER': 'Player',
        'COURT_OWNER': 'Court Owner',
        'COURT_MANAGER': 'Court Manager',
        'SUPER_USER': 'Administrator'
    };
    return roleMap[user.value.role] || 'Player';
});

const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

const fetchPlayerStats = async () => {
    if (user.value.role !== 'PLAYER') return;

    try {
        stats.value = {
            total_bookings: 15,
            total_matches_played: 8,
            matches_won: 5,
            matches_lost: 3,
            sportsmanship_rating: 4.5
        };
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
};

const handleUpdateProfile = async () => {
    loading.value = true;
    successMessage.value = '';
    errorMessage.value = '';

    try {
        const response = await apiClient.patch('/user/profile/', profileForm.value);

        user.value = response.data;
        authStore.user = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));

        successMessage.value = 'Profile updated successfully!';
        editMode.value = false;

        setTimeout(() => {
            successMessage.value = '';
        }, 3000);
    } catch (error) {
        errorMessage.value = error.response?.data?.detail || 'Failed to update profile';
        setTimeout(() => {
            errorMessage.value = '';
        }, 5000);
    } finally {
        loading.value = false;
    }
};

const cancelEdit = () => {
    profileForm.value = {
        full_name: user.value.full_name || '',
        email: user.value.email || '',
        phone_number: user.value.phone_number || '',
        date_of_birth: user.value.date_of_birth || '',
        city: user.value.city || '',
        address: user.value.address || '',
    };
    editMode.value = false;
    errorMessage.value = '';
};

const handleLogout = async () => {
    await authStore.logout();
    router.push('/login');
};

onMounted(() => {
    fetchPlayerStats();
});
</script>

<style scoped>
:root {
    /* Primary Colors */
    --color-primary-base: #0056B3;
    --color-primary-light: #E3F2FD;
    --color-primary-dark: #003D82;

    /* Secondary Colors */
    --color-charcoal: #1F2937;
    --color-light-gray: #F3F4F6;
    --color-white: #FFFFFF;

    /* Accent Colors */
    --color-accent-purple: #7C3AED;
    --color-accent-muted: #9CA3AF;

    /* Status Colors */
    --color-success: #10B981;
    --color-warning: #F59E0B;
    --color-alert: #EF4444;

    /* CTA Colors */
    --color-cta-primary: #FF6B35;
    --color-cta-secondary: #0056B3;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.profile-container {
    min-height: 100vh;
    background: linear-gradient(135deg, var(--color-light-gray) 0%, #FFFFFF 100%);
}

/* Header Styles */
.profile-header {
    background: linear-gradient(135deg, var(--color-primary-base) 0%, var(--color-accent-purple) 100%);
    color: var(--color-white);
    padding: 32px 0;
    box-shadow: 0 8px 24px rgba(0, 86, 179, 0.2);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}

.header-title {
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.5px;
    flex: 1;
    text-align: center;
}

.header-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 8px;
    color: var(--color-white);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
}

.header-btn:hover {
    background: rgba(255, 255, 255, 0.25);
    border-color: rgba(255, 255, 255, 0.35);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Profile Content */
.profile-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 48px 20px;
    display: flex;
    flex-direction: column;
    gap: 32px;
}

/* Profile Picture Section */
.profile-picture-section {
    background: var(--color-white);
    border-radius: 20px;
    padding: 48px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    border: 1px solid var(--color-light-gray);
    transition: box-shadow 0.3s ease;
}

.profile-picture-section:hover {
    box-shadow: 0 8px 32px rgba(0, 86, 179, 0.12);
}

.avatar-container {
    position: relative;
}

.avatar-wrapper {
    position: relative;
    display: inline-block;
}

.avatar {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    object-fit: cover;
    border: 5px solid var(--color-primary-base);
    box-shadow: 0 8px 24px rgba(0, 86, 179, 0.3);
    transition: transform 0.3s ease;
}

.avatar:hover {
    transform: scale(1.02);
}

.avatar-placeholder {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--color-primary-base) 0%, var(--color-accent-purple) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56px;
    font-weight: 700;
    color: var(--color-white);
    box-shadow: 0 8px 24px rgba(0, 86, 179, 0.3);
}

.edit-avatar-btn {
    position: absolute;
    bottom: 8px;
    right: 8px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--color-white);
    border: 2px solid var(--color-cta-primary);
    color: var(--color-cta-primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.2);
    font-size: 0;
}

.edit-avatar-btn:hover {
    background: var(--color-cta-primary);
    color: var(--color-white);
    transform: scale(1.15);
    box-shadow: 0 6px 20px rgba(255, 107, 53, 0.35);
}

.user-info {
    text-align: center;
}

.user-info h2 {
    font-size: 28px;
    font-weight: 700;
    color: var(--color-charcoal);
    margin-bottom: 12px;
    letter-spacing: -0.5px;
}

.role-badge {
    display: inline-block;
    padding: 8px 20px;
    border-radius: 24px;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.role-player {
    background: #DCFCE7;
    color: #166534;
}

.role-owner {
    background: #FEF08A;
    color: #854D0E;
}

.role-manager {
    background: #DBEAFE;
    color: #1E40AF;
}

.role-admin {
    background: #FECACA;
    color: #991B1B;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
}

.stat-card {
    background: var(--color-white);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
    display: flex;
    align-items: center;
    gap: 20px;
    border: 1px solid var(--color-light-gray);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 28px rgba(0, 86, 179, 0.12);
    border-color: var(--color-primary-light);
}

.stat-icon {
    width: 64px;
    height: 64px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-white);
    flex-shrink: 0;
    font-size: 0;
}

.stat-icon.bookings {
    background: linear-gradient(135deg, var(--color-primary-base) 0%, #0088CC 100%);
}

.stat-icon.points {
    background: linear-gradient(135deg, var(--color-accent-purple) 0%, #9F7AEA 100%);
}

.stat-icon.matches {
    background: linear-gradient(135deg, var(--color-cta-primary) 0%, #FF8C42 100%);
}

.stat-icon.rating {
    background: linear-gradient(135deg, var(--color-success) 0%, #34D399 100%);
}

.stat-content {
    flex: 1;
}

.stat-content h3 {
    font-size: 14px;
    font-weight: 600;
    color: var(--color-accent-muted);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: var(--color-charcoal);
}

/* Profile Section */
.profile-section {
    background: var(--color-white);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--color-light-gray);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 2px solid var(--color-light-gray);
}

.section-header h3 {
    font-size: 20px;
    font-weight: 700;
    color: var(--color-charcoal);
    letter-spacing: -0.5px;
}

.edit-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: var(--color-primary-light);
    border: 1px solid var(--color-primary-base);
    border-radius: 8px;
    color: var(--color-primary-base);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.edit-btn:hover {
    background: var(--color-primary-base);
    color: var(--color-white);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 86, 179, 0.2);
}

/* Alerts */
.alert {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 24px;
    animation: slideDown 0.3s ease;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.alert-success {
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #D1FAE5;
}

.alert-error {
    background: #FEF2F2;
    color: #991B1B;
    border: 1px solid #FECACA;
}

/* Form Styles */
.profile-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.form-row:last-of-type {
    grid-template-columns: 1fr;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 14px;
    font-weight: 600;
    color: var(--color-charcoal);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.input-wrapper svg {
    position: absolute;
    left: 16px;
    color: var(--color-accent-muted);
    pointer-events: none;
}

.input-wrapper input,
.input-wrapper textarea {
    width: 100%;
    padding: 12px 16px 12px 48px;
    border: 2px solid var(--color-light-gray);
    border-radius: 10px;
    font-size: 14px;
    color: var(--color-charcoal);
    background: var(--color-white);
    transition: all 0.3s ease;
    font-family: inherit;
}

.input-wrapper input:hover,
.input-wrapper textarea:hover {
    border-color: var(--color-primary-light);
}

.input-wrapper input:focus,
.input-wrapper textarea:focus {
    outline: none;
    border-color: var(--color-primary-base);
    box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
    background: var(--color-primary-light);
}

.input-wrapper input:disabled,
.input-wrapper textarea:disabled {
    background: var(--color-light-gray);
    color: var(--color-accent-muted);
    cursor: not-allowed;
}

.field-hint {
    font-size: 12px;
    color: var(--color-accent-muted);
    font-weight: 500;
}

.form-actions {
    display: flex;
    gap: 16px;
    padding-top: 20px;
    justify-content: flex-end;
}

.btn {
    padding: 12px 28px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn-primary {
    background: linear-gradient(135deg, var(--color-cta-primary) 0%, #FF8C42 100%);
    color: var(--color-white);
    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4);
}

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-secondary {
    background: var(--color-light-gray);
    color: var(--color-charcoal);
    border: 2px solid var(--color-primary-base);
}

.btn-secondary:hover {
    background: var(--color-primary-light);
    transform: translateY(-2px);
}

/* Status Grid */
.status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
}

.status-item {
    background: var(--color-light-gray);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    transition: all 0.3s ease;
}

.status-item:hover {
    background: var(--color-primary-light);
    border-color: var(--color-primary-base);
}

.status-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--color-accent-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

.status-value {
    font-size: 16px;
    font-weight: 700;
    color: var(--color-charcoal);
}

/* Badges */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    width: fit-content;
}

.badge-success {
    background: #D1FAE5;
    color: #065F46;
}

.badge-warning {
    background: #FEF3C7;
    color: #92400E;
}

.badge-error {
    background: #FECACA;
    color: #991B1B;
}

/* Responsive Design */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        gap: 16px;
    }

    .header-title {
        font-size: 24px;
        order: 2;
    }

    .back-btn {
        order: 1;
        align-self: flex-start;
    }

    .logout-btn {
        order: 3;
        align-self: flex-start;
    }

    .profile-content {
        padding: 24px 16px;
        gap: 24px;
    }

    .profile-picture-section {
        padding: 32px 20px;
    }

    .avatar {
        width: 100px;
        height: 100px;
    }

    .avatar-placeholder {
        width: 100px;
        height: 100px;
        font-size: 42px;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .form-actions {
        flex-direction: column;
        justify-content: stretch;
    }

    .btn {
        width: 100%;
    }

    .section-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
    }

    .edit-btn {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .profile-header {
        padding: 20px 0;
    }

    .header-title {
        font-size: 20px;
    }

    .header-btn {
        font-size: 12px;
        padding: 8px 12px;
    }

    .user-info h2 {
        font-size: 22px;
    }

    .stat-number {
        font-size: 24px;
    }

    .status-grid {
        grid-template-columns: 1fr;
    }

    .profile-section {
        padding: 20px;
    }

    .section-header h3 {
        font-size: 18px;
    }
}
</style>