<!-- components/StatCard.vue -->
<template>
    <div class="bg-white rounded-2xl shadow-md border border-emerald-100 p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-sm font-medium text-gray-600">{{ title }}</p>
                <p :class="[
                    'text-3xl font-bold mt-2',
                    highlight ? 'text-red-600' : `text-${color}-700`
                ]">
                    {{ value }}
                </p>
            </div>
            <div :class="`w-14 h-14 rounded-xl bg-${color}-100 flex items-center justify-center text-2xl`">
                {{ icon }}
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: {
        type: String,
        required: true
    },
    value: {
        type: [String, Number],
        required: true
    },
    icon: {
        type: String,
        required: true
    },
    color: {
        type: String,
        default: 'emerald'
    },
    highlight: {
        type: Boolean,
        default: false
    }
})
</script>