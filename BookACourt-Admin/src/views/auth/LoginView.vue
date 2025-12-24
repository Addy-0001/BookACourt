<template>
    <div class="login-page">
        <div class="login-container">
            <div class="login-card">
                <!-- Logo & Title -->
                <div class="login-header">
                    <div class="logo">🏟️</div>
                    <h1>BookACourt Admin</h1>
                    <p class="subtitle">Sign in to manage your courts</p>
                </div>

                <!-- Error Alert -->
                <div v-if="errorMessage" class="alert alert-error">
                    <span class="alert-icon">⚠️</span>
                    <span>{{ errorMessage }}</span>
                </div>

                <!-- Login Form -->
                <form @submit.prevent="handleLogin" class="login-form">
                    <div class="form-group">
                        <label for="phone">Phone Number</label>
                        <div class="input-wrapper">
                            <span class="input-icon">📱</span>
                            <input id="phone" v-model="loginForm.phone_number" type="tel" placeholder="+977 9812345678"
                                required :disabled="loading" />
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="password">Password</label>
                        <div class="input-wrapper">
                            <span class="input-icon">🔒</span>
                            <input id="password" v-model="loginForm.password" :type="showPassword ? 'text' : 'password'"
                                placeholder="Enter your password" required :disabled="loading" />
                            <button type="button" class="toggle-password" @click="showPassword = !showPassword"
                                tabindex="-1">
                                {{ showPassword ? '👁️' : '👁️‍🗨️' }}
                            </button>
                        </div>
                    </div>

                    <div class="form-options">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="rememberMe" />
                            <span>Remember me</span>
                        </label>
                        <router-link to="/forgot-password" class="link">
                            Forgot password?
                        </router-link>
                    </div>

                    <button type="submit" class="btn-login" :disabled="loading">
                        <span v-if="loading" class="spinner-small"></span>
                        <span v-else>Sign In</span>
                    </button>
                </form>

                <!-- Divider -->
                <div class="divider">
                    <span>or</span>
                </div>

                <!-- Sign Up Link -->
                <div class="signup-link">
                    <p>Don't have an account?</p>
                    <router-link to="/register" class="btn-signup">
                        Create Account
                    </router-link>
                </div>
            </div>

            <!-- Footer -->
            <div class="login-footer">
                <p>&copy; 2024 BookACourt. All rights reserved.</p>
                <div class="footer-links">
                    <a href="#">Terms</a>
                    <span>•</span>
                    <a href="#">Privacy</a>
                    <span>•</span>
                    <a href="#">Help</a>
                </div>
            </div>
        </div>

        <!-- Background Design -->
        <div class="login-background">
            <div class="bg-shape shape-1"></div>
            <div class="bg-shape shape-2"></div>
            <div class="bg-shape shape-3"></div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

// State
const loginForm = ref({
    phone_number: '',
    password: '',
});
const showPassword = ref(false);
const rememberMe = ref(false);
const loading = ref(false);
const errorMessage = ref('');

// Methods
async function handleLogin() {
    loading.value = true;
    errorMessage.value = '';

    try {
        const response = await axios.post('http://localhost:8000/api/auth/login/', {
            phone_number: loginForm.value.phone_number,
            password: loginForm.value.password,
        });

        // Store tokens and user info
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        localStorage.setItem('user', JSON.stringify(response.data.user));

        // Check if user has admin privileges
        const userRole = response.data.user.role;
        if (!['SUPER_USER', 'COURT_OWNER', 'COURT_MANAGER'].includes(userRole)) {
            throw new Error('You do not have permission to access the admin panel');
        }

        // Redirect to dashboard
        router.push('/');
    } catch (error) {
        console.error('Login error:', error);
        errorMessage.value =
            error.message ||
            error.response?.data?.detail ||
            'Invalid phone number or password';
    } finally {
        loading.value = false;
    }
}
</script>

<style scoped>
.login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container {
    position: relative;
    z-index: 10;
    width: 100%;
    max-width: 440px;
    padding: 2rem;
}

.login-card {
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    padding: 3rem 2.5rem;
    animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
}

.logo {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: bounce 1s ease-in-out;
}

@keyframes bounce {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10px);
    }
}

.login-header h1 {
    font-size: 1.75rem;
    color: #2c3e50;
    margin: 0 0 0.5rem 0;
    font-weight: 700;
}

.subtitle {
    color: #7f8c8d;
    font-size: 0.95rem;
    margin: 0;
}

/* Alert */
.alert {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    animation: shake 0.5s;
}

@keyframes shake {

    0%,
    100% {
        transform: translateX(0);
    }

    25% {
        transform: translateX(-10px);
    }

    75% {
        transform: translateX(10px);
    }
}

.alert-error {
    background: #fee;
    color: #c0392b;
    border: 1px solid #e74c3c;
}

.alert-icon {
    font-size: 1.25rem;
}

/* Form */
.login-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
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

.input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.input-icon {
    position: absolute;
    left: 1rem;
    font-size: 1.25rem;
    pointer-events: none;
}

.input-wrapper input {
    width: 100%;
    padding: 0.875rem 1rem 0.875rem 3rem;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    font-size: 0.95rem;
    transition: all 0.2s;
    font-family: inherit;
}

.input-wrapper input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-wrapper input:disabled {
    background: #f5f5f5;
    cursor: not-allowed;
}

.toggle-password {
    position: absolute;
    right: 1rem;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.25rem;
    padding: 0.25rem;
    transition: opacity 0.2s;
}

.toggle-password:hover {
    opacity: 0.7;
}

.form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.9rem;
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    color: #2c3e50;
}

.checkbox-label input {
    cursor: pointer;
}

.link {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.link:hover {
    color: #764ba2;
    text-decoration: underline;
}

.btn-login {
    padding: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    margin-top: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 48px;
}

.btn-login:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.btn-login:active:not(:disabled) {
    transform: translateY(0);
}

.btn-login:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.spinner-small {
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* Divider */
.divider {
    position: relative;
    text-align: center;
    margin: 1.5rem 0;
    color: #7f8c8d;
    font-size: 0.9rem;
}

.divider::before,
.divider::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 40%;
    height: 1px;
    background: #e0e0e0;
}

.divider::before {
    left: 0;
}

.divider::after {
    right: 0;
}

.divider span {
    background: white;
    padding: 0 1rem;
    position: relative;
}

/* Sign Up */
.signup-link {
    text-align: center;
}

.signup-link p {
    color: #7f8c8d;
    margin: 0 0 0.75rem 0;
    font-size: 0.9rem;
}

.btn-signup {
    display: inline-block;
    padding: 0.75rem 2rem;
    background: white;
    color: #667eea;
    border: 2px solid #667eea;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s;
}

.btn-signup:hover {
    background: #667eea;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

/* Footer */
.login-footer {
    text-align: center;
    margin-top: 2rem;
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.85rem;
}

.login-footer p {
    margin: 0 0 0.5rem 0;
}

.footer-links {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.footer-links a {
    color: rgba(255, 255, 255, 0.9);
    text-decoration: none;
    transition: color 0.2s;
}

.footer-links a:hover {
    color: white;
    text-decoration: underline;
}

/* Background */
.login-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 1;
}

.bg-shape {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(50px);
}

.shape-1 {
    width: 400px;
    height: 400px;
    top: -200px;
    left: -100px;
    animation: float 15s ease-in-out infinite;
}

.shape-2 {
    width: 300px;
    height: 300px;
    bottom: -150px;
    right: -50px;
    animation: float 12s ease-in-out infinite reverse;
}

.shape-3 {
    width: 200px;
    height: 200px;
    top: 50%;
    right: 10%;
    animation: float 18s ease-in-out infinite;
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0) rotate(0deg);
    }

    50% {
        transform: translateY(-20px) rotate(180deg);
    }
}

/* Responsive */
@media (max-width: 768px) {
    .login-container {
        padding: 1rem;
    }

    .login-card {
        padding: 2rem 1.5rem;
    }

    .logo {
        font-size: 3rem;
    }

    .login-header h1 {
        font-size: 1.5rem;
    }
}
</style>