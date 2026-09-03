<template>
  <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
    <input
      :value="search"
      @input="$emit('update:search', $event.target.value); $emit('change')"
      type="text"
      placeholder="Cari judul atau deskripsi..."
      class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 md:col-span-2"
    />

    <select
      :value="status"
      @change="$emit('update:status', $event.target.value); $emit('change')"
      class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="">Semua status</option>
      <option value="pending">Pending</option>
      <option value="progress">Progress</option>
      <option value="done">Done</option>
    </select>

    <select
      :value="priority"
      @change="$emit('update:priority', $event.target.value); $emit('change')"
      class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="">Semua priority</option>
      <option value="low">Low</option>
      <option value="medium">Medium</option>
      <option value="high">High</option>
    </select>

    <select
      :value="`${sortBy}:${sortOrder}`"
      @change="onSortChange"
      class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="created_at:desc">Terbaru dibuat</option>
      <option value="created_at:asc">Terlama dibuat</option>
      <option value="updated_at:desc">Terbaru diperbarui</option>
      <option value="title:asc">Judul A–Z</option>
      <option value="title:desc">Judul Z–A</option>
      <option value="priority:desc">Prioritas tertinggi</option>
      <option value="priority:asc">Prioritas terendah</option>
    </select>
  </div>
</template>

<script setup>
defineProps(['search', 'status', 'priority', 'sortBy', 'sortOrder'])
const emit = defineEmits([
  'update:search',
  'update:status',
  'update:priority',
  'update:sortBy',
  'update:sortOrder',
  'change',
])

function onSortChange(e) {
  const [sortBy, sortOrder] = e.target.value.split(':')
  emit('update:sortBy', sortBy)
  emit('update:sortOrder', sortOrder)
  emit('change')
}
</script>
