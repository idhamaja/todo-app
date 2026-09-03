<template>
  <div class="fixed bottom-4 right-4 z-50">
    <div
      class="px-4 py-3 rounded-md shadow-lg text-sm text-white flex items-center gap-3"
      :class="type === 'error' ? 'bg-red-600' : 'bg-emerald-600'"
    >
      <span>{{ message }}</span>
      <button class="opacity-70 hover:opacity-100" @click="$emit('close')">&times;</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: { type: String, default: 'success' },
  message: { type: String, required: true },
})
defineEmits(['close'])
</script>
