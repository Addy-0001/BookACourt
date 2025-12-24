<template>
    <div class="register-page">
        <div class="register-container">
            <div class="register-card">
                <!-- Logo & Title -->
                <div class="register-header">
                    <div class="logo">🏟️</div>
                    <h1>Create Admin Account</h1>
                    <p class="subtitle">Register to manage courts</p>
                </div>

                <!-- Error/Success Alert -->
                <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
                    <span class="alert-icon">{{ message.type === 'error' ? '⚠️' : '✅' }}</span>
                    <span>{{ message.text }}</span>
                </div>

                <!-- Register Form -->
                <form @submit.prevent="handleRegister" class="register-form">
                    <div class="form-group">
                        <label for="full_name">Full Name *</label>
                        <input id="full_name" v-model="registerForm.full_name" type="text" placeholder="John Doe"
                            required :disabled="loading" />
                    </div>

                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input id="phone" v-model="registerForm.phone_number" type="tel" placeholder="+977 9812345678"
                            required :disabled="loading" />
                    </div>

                    <div class="form-group">
                        <label for="email">Email</label>
                        <input id="email" v-model="registerForm.email" type="email" placeholder="john@example.com"
                            :disabled="loading" />
                    </div>

                    <div class="form-group">
                        <label for="role">Account Type *</label>
                        <select id="role" v-model="registerForm.role" required :disabled="loading">
                            <option value="COURT_OWNER">Court Owner</option>
                            <option value="COURT_MANAGER">Court Manager</option>
                        </select>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="password1">Password *</label>
                            <input id="password1" v-model="registerForm.password1" type="password"
                                placeholder="••••••••" required :disabled="loading" />
                        </div>

                        <div class="form-group">
                            <label for="password2">Confirm Password *</label>
                            <input id="password2" v-model="registerForm.password2" type="password"
                                placeholder="••••••••" required :disabled="loading" />
                        </div>
                    </div>

                    <div class="form-group checkbox-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="agreedToTerms" required />
                            <span>I agree to the <a href="#" class="link">Terms & Conditions</a></span>
                        </label>
                    </div>

                    <button type="submit" class="btn-register" :disabled="loading || !agreedToTerms">
                        <span v-if="loading" class="spinner-small"></span>
                        <span v-else>Create Account</span>
                    </button>
                </form>

                <!-- Login Link -->
                <div class="login-link">
                    <p>Already have an account?</p>
                    <router-link to="/login" class="link-primary">
                        Sign In
                    </router-link>
                </div>
            </div>

            <!-- Footer -->
            <div class="register-footer">
                <p>&copy; 2024 BookACourt. All rights reserved.</p>
            </div>
        </div>

        <!-- Background Design -->
        <div class="register-background">
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
const registerForm = ref({
    full_name: '',
    phone_number: '',
    email: '',
    password1: '',
    password2: '',
    role: 'COURT_OWNER',
});
const agreedToTerms = ref(false);
const loading = ref(false);
const message = ref({ type: '', text: '' });

// Methods
async function handleRegister() {
    loading.value = true;
    message.value = { type: '', text: '' };

    // Validate passwords match
    if (registerForm.value.password1 !== registerForm.value.password2) {
        message.value = { type: 'error', text: 'Passwords do not match' };
        loading.value = false;
        return;
    }

    try {
        const response = await axios.post('http://localhost:8000/api/auth/register/', registerForm.value);

        message.value = {
            type: 'success',
            text: 'Account created successfully! Redirecting to login...'
        };

        // Redirect to login after 2 seconds
        setTimeout(() => {
            router.push('/login');
        }, 2000);
    } catch (error) {
        console.error('Register error:', error);

        // Handle validation errors
        if (error.response?.data) {
            const errors = error.response.data;
            const errorMessages = [];

            for (const [field, messages] of Object.entries(errors)) {
                if (Array.isArray(messages)) {
                    errorMessages.push(...messages);
                } else {
                    errorMessages.push(messages);
                }
            }

            message.value = {
                type: 'error',
                text: errorMessages.join('. ') || 'Registration failed'
            };
        } else {
            message.value = {
                type: 'error',
                text: 'Registration failed. Please try again.'
            };
        }
    } finally {
        loading.value = false;
    }
}
</script>

<style scoped>
.register-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem 0;
}

.register-container {
    position: relative;
    z-index: 10;
    width: 100%;
    max-width: 600px;
    padding: 2rem;
}

.register-card {
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

.register-header {
    text-align: center;
    margin-bottom: 2rem;
}

.logo {
    font-size: 3.5rem;
    margin-bottom: 1rem;
}

.register-header h1 {
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
    animation: slideDown 0.3s ease-out;
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

.alert-error {
    background: #fee;
    color: #c0392b;
    border: 1px solid #e74c3c;
}

.alert-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #28a745;
}

.alert-icon {
    font-size: 1.25rem;
}

/* Form */
.register-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
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
.form-group select {
    padding: 0.875rem 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    font-size: 0.95rem;
    transition: all 0.2s;
    font-family: inherit;
}

.form-group input:focus,
.form-group select:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled,
.form-group select:disabled {
    background: #f5f5f5;
    cursor: not-allowed;
}

.checkbox-group {
    margin-top: 0.5rem;
}

.checkbox-label {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    cursor: pointer;
    color: #2c3e50;
    font-size: 0.9rem;
}

.checkbox-label input {
    margin-top: 0.25rem;
    cursor: pointer;
}

.link {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.link:hover {
    text-decoration: underline;
}

.btn-register {
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

.btn-register:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.btn-register:disabled {
    opacity: 0.6;
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

/* Login Link */
.login-link {
    text-align: center;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e0e0e0;
}

.login-link p {
    color: #7f8c8d;
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
}

.link-primary {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
    font-size: 1rem;
}

.link-primary:hover {
    text-decoration: underline;
}

/* Footer */
.register-footer {
    text-align: center;
    margin-top: 1.5rem;
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.85rem;
}

/* Background */
.register-background {
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
    .register-container {
        padding: 1rem;
    }

    .register-card {
        padding: 2rem 1.5rem;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .logo {
        font-size: 3rem;
    }

    .register-header h1 {
        font-size: 1.5rem;
    }
}
</style>