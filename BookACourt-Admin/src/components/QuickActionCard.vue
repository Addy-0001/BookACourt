<!-- components/QuickActionCard.vue -->
<template>
    <router-link :to="to"
        class="block bg-white rounded-2xl shadow-md border border-emerald-100 p-6 hover:shadow-xl hover:border-emerald-300 transition-all group">
        <div class="flex items-center gap-4 mb-4">
            <div
                class="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center text-2xl text-emerald-600 group-hover:bg-emerald-200 transition-colors">
                {{ icon }}
            </div>
            <div>
                <h3 class="text-xl font-bold text-gray-900 group-hover:text-emerald-700 transition-colors">
                    {{ title }}
                </h3>
                <p class="text-sm text-gray-600 mt-1">{{ description }}</p>
            </div>
        </div>

        <span v-if="badge > 0" class="inline-flex px-3 py-1 bg-red-100 text-red-800 rounded-full text-xs font-semibold">
            {{ badge }} pending
        </span>
    </router-link>
</template>

<script setup>
defineProps({
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    },
    icon: {
        type: String,
        required: true
    },
    to: {
        type: String,
        required: true
    },
    badge: {
        type: Number,
        default: 0
    }
})
</script>