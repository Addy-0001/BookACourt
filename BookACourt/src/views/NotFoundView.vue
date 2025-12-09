<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center px-4">
        <div class="text-center">
            <div class="mb-8">
                <svg class="w-64 h-64 mx-auto text-blue-600 opacity-50" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
            <h1 class="text-6xl font-bold text-gray-900 mb-4">404</h1>
            <p class="text-2xl font-semibold text-gray-700 mb-2">Page Not Found</p>
            <p class="text-gray-600 mb-8 max-w-md mx-auto">
                Sorry, the page you're looking for doesn't exist or has been moved.
            </p>
            <div class="flex items-center justify-center gap-4">
                <button @click="goBack"
                    class="px-6 py-3 bg-white text-blue-600 border-2 border-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
                    Go Back
                </button>
                <router-link to="/"
                    class="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                    Go Home
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
    router.go(-1)
}
</script>