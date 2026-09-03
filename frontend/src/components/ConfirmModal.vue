<template>
  <div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-sm w-full p-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-2">{{ title }}</h3>
      <p class="text-gray-500 text-sm mb-6">{{ message }}</p>
      <div class="flex justify-end gap-2">
        <button
          class="px-4 py-2 text-sm rounded-md border border-gray-300 hover:bg-gray-50"
          @click="$emit('cancel')"
        >
          Batal
        </button>
        <button
          class="px-4 py-2 text-sm rounded-md bg-red-600 text-white hover:bg-red-700"
          @click="$emit('confirm')"
        >
          Hapus
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  message: { type: String, required: true },
})
defineEmits(['cancel', 'confirm'])
</script>
