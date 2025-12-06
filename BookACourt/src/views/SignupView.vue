<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <h1>Create Account</h1>
                <p>Join BookACourt today</p>
            </div>

            <form @submit.prevent="handleSignup" class="auth-form">
                <div v-if="error" class="alert alert-error">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    {{ error }}
                </div>

                <div v-if="success" class="alert alert-success">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    Registration successful! Redirecting to login...
                </div>

                <div class="form-group">
                    <label for="fullname">Full Name</label>
                    <div class="input-wrapper">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        <input id="fullname" v-model="signupForm.full_name" type="text" placeholder="John Doe"
                            required />
                    </div>
                </div>

                <div class="form-group">
                    <label for="phone">Phone Number</label>
                    <div class="input-wrapper">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path
                                d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                            </path>
                        </svg>
                        <input id="phone" v-model="signupForm.phone_number" type="tel" placeholder="+977 9800000000"
                            required />
                    </div>
                </div>

                <div class="form-group">
                    <label for="email">Email (Optional)</label>
                    <div class="input-wrapper">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z">
                            </path>
                            <polyline points="22,6 12,13 2,6"></polyline>
                        </svg>
                        <input id="email" v-model="signupForm.email" type="email" placeholder="john@example.com" />
                    </div>
                </div>

                <div class="form-group">
                    <label for="role">I am a</label>
                    <div class="input-wrapper">
                        <select id="role" v-model="signupForm.role" required>
                            <option value="PLAYER">Player</option>
                            <option value="COURT_OWNER">Court Owner</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label for="password1">Password</label>
                    <div class="input-wrapper">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                        </svg>
                        <input id="password1" v-model="signupForm.password1" :type="showPassword ? 'text' : 'password'"
                            placeholder="Create a password" required />
                        <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                            <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                                viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                stroke-linecap="round" stroke-linejoin="round">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                <circle cx="12" cy="12" r="3"></circle>
                            </svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round">
                                <path
                                    d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24">
                                </path>
                                <line x1="1" y1="1" x2="23" y2="23"></line>
                            </svg>
                        </button>
                    </div>
                </div>

                <div class="form-group">
                    <label for="password2">Confirm Password</label>
                    <div class="input-wrapper">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                        </svg>
                        <input id="password2" v-model="signupForm.password2" :type="showPassword ? 'text' : 'password'"
                            placeholder="Confirm your password" required />
                    </div>
                </div>

                <button type="submit" class="btn btn-primary" :disabled="loading">
                    <span v-if="loading">Creating account...</span>
                    <span v-else>Sign Up</span>
                </button>

                <div class="auth-footer">
                    <p>Already have an account? <router-link to="/login">Login</router-link></p>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const signupForm = ref({
    phone_number: '',
    full_name: '',
    email: '',
    password1: '',
    password2: '',
    role: 'PLAYER',
});

const showPassword = ref(false);
const loading = ref(false);
const error = ref('');
const success = ref(false);

const handleSignup = async () => {
    loading.value = true;
    error.value = '';
    success.value = false;

    // Validate passwords match
    if (signupForm.value.password1 !== signupForm.value.password2) {
        error.value = 'Passwords do not match';
        loading.value = false;
        return;
    }

    try {
        await authStore.register(signupForm.value);
        success.value = true;

        setTimeout(() => {
            router.push('/login');
        }, 2000);
    } catch (err) {
        const errorData = err.response?.data;
        if (errorData) {
            if (typeof errorData === 'object') {
                error.value = Object.values(errorData).flat().join(' ');
            } else {
                error.value = errorData;
            }
        } else {
            error.value = 'Registration failed. Please try again.';
        }
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
}

.auth-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    padding: 40px;
    width: 100%;
    max-width: 440px;
}

.auth-header {
    text-align: center;
    margin-bottom: 32px;
}

.auth-header h1 {
    font-size: 28px;
    font-weight: 700;
    color: #1a202c;
    margin-bottom: 8px;
}

.auth-header p {
    font-size: 16px;
    color: #718096;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.alert {
    padding: 12px 16px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
}

.alert-error {
    background: #fee;
    color: #c53030;
    border: 1px solid #fc8181;
}

.alert-success {
    background: #e6fffa;
    color: #047857;
    border: 1px solid #6ee7b7;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 14px;
    font-weight: 600;
    color: #2d3748;
}

.input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.input-wrapper svg {
    position: absolute;
    left: 12px;
    color: #a0aec0;
    pointer-events: none;
    z-index: 1;
}

.input-wrapper input,
.input-wrapper select {
    width: 100%;
    padding: 12px 12px 12px 44px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 16px;
    transition: all 0.2s;
}

.input-wrapper select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%23a0aec0' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    padding-right: 40px;
}

.input-wrapper input:focus,
.input-wrapper select:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.toggle-password {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    color: #a0aec0;
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    z-index: 1;
}

.toggle-password:hover {
    color: #667eea;
}

.btn {
    padding: 14px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.auth-footer {
    text-align: center;
    margin-top: 8px;
}

.auth-footer p {
    font-size: 14px;
    color: #718096;
}

.auth-footer a {
    color: #667eea;
    font-weight: 600;
    text-decoration: none;
}

.auth-footer a:hover {
    text-decoration: underline;
}
</style>