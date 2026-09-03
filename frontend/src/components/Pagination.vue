<template>
  <div class="flex flex-col sm:flex-row justify-between items-center gap-3 mt-4 text-sm text-gray-600">
    <div>
      Halaman <span class="font-medium text-gray-800">{{ page }}</span> dari
      <span class="font-medium text-gray-800">{{ totalPages }}</span>
      &middot; {{ total }} total data
    </div>
    <div class="flex gap-1">
      <button
        class="px-3 py-1.5 rounded-md border border-gray-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-100"
        :disabled="page <= 1"
        @click="$emit('change-page', page - 1)"
      >
        &larr; Prev
      </button>
      <button
        class="px-3 py-1.5 rounded-md border border-gray-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-100"
        :disabled="page >= totalPages"
        @click="$emit('change-page', page + 1)"
      >
        Next &rarr;
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true },
  total: { type: Number, required: true },
  pageSize: { type: Number, required: true },
})
defineEmits(['change-page'])
</script>
