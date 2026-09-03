<template>
  <div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-lg w-full p-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        {{ isEdit ? 'Edit Todo' : 'Tambah Todo' }}
      </h3>

      <form @submit.prevent="handleSubmit" novalidate>
        <!-- Title -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Title <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.title"
            type="text"
            maxlength="255"
            class="w-full border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2"
            :class="errors.title ? 'border-red-400 focus:ring-red-300' : 'border-gray-300 focus:ring-blue-500'"
            placeholder="Judul todo"
            @blur="validateField('title')"
          />
          <div class="flex justify-between mt-1">
            <p v-if="errors.title" class="text-xs text-red-500">{{ errors.title }}</p>
            <p class="text-xs text-gray-400 ml-auto">{{ form.title.length }}/255</p>
          </div>
        </div>

        <!-- Status & Priority -->
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              v-model="form.status"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="pending">Pending</option>
              <option value="progress">Progress</option>
              <option value="done">Done</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select
              v-model="form.priority"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        <!-- Description -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            v-model="form.description"
            rows="3"
            maxlength="2000"
            class="w-full border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2"
            :class="errors.description ? 'border-red-400 focus:ring-red-300' : 'border-gray-300 focus:ring-blue-500'"
            placeholder="Deskripsi (opsional)"
            @blur="validateField('description')"
          ></textarea>
          <div class="flex justify-between mt-1">
            <p v-if="errors.description" class="text-xs text-red-500">{{ errors.description }}</p>
            <p class="text-xs text-gray-400 ml-auto">{{ (form.description || '').length }}/2000</p>
          </div>
        </div>

        <p v-if="serverError" class="text-xs text-red-500 mb-3">{{ serverError }}</p>

        <div class="flex justify-end gap-2 mt-6">
          <button
            type="button"
            class="px-4 py-2 text-sm rounded-md border border-gray-300 hover:bg-gray-50"
            @click="$emit('close')"
          >
            Batal
          </button>
          <button
            type="submit"
            class="px-4 py-2 text-sm rounded-md bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            :disabled="submitting"
          >
            {{ submitting ? 'Menyimpan...' : 'Simpan' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import api from '../api'

const props = defineProps({
  todo: { type: Object, default: null },
})
const emit = defineEmits(['close', 'saved'])

const isEdit = computed(() => !!props.todo)

const form = reactive({
  title: props.todo?.title ?? '',
  status: props.todo?.status ?? 'pending',
  priority: props.todo?.priority ?? 'medium',
  description: props.todo?.description ?? '',
})

const errors = reactive({ title: '', description: '' })
const serverError = ref('')
const submitting = ref(false)

function validateField(field) {
  if (field === 'title') {
    const trimmed = form.title.trim()
    if (!trimmed) {
      errors.title = 'Title wajib diisi'
    } else if (trimmed.length > 255) {
      errors.title = 'Title maksimal 255 karakter'
    } else {
      errors.title = ''
    }
  }
  if (field === 'description') {
    if (form.description && form.description.length > 2000) {
      errors.description = 'Deskripsi maksimal 2000 karakter'
    } else {
      errors.description = ''
    }
  }
}

function validateAll() {
  validateField('title')
  validateField('description')
  return !errors.title && !errors.description
}

async function handleSubmit() {
  serverError.value = ''
  if (!validateAll()) return

  submitting.value = true
  const payload = {
    title: form.title.trim(),
    status: form.status,
    priority: form.priority,
    description: form.description ? form.description.trim() : null,
  }

  try {
    if (isEdit.value) {
      await api.updateTodo(props.todo.id, payload)
      emit('saved', 'Todo berhasil diperbarui')
    } else {
      await api.createTodo(payload)
      emit('saved', 'Todo berhasil ditambahkan')
    }
  } catch (err) {
    serverError.value = extractServerError(err)
  } finally {
    submitting.value = false
  }
}

function extractServerError(err) {
  const detail = err?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg || JSON.stringify(d)).join(', ')
  }
  return 'Gagal menyimpan data, silakan coba lagi.'
}
</script>
