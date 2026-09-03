<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-6xl mx-auto">
      <header class="mb-6">
        <h1 class="text-3xl font-bold text-gray-800">Todo List</h1>
        <p class="text-gray-500 mt-1 text-sm">Kelola daftar tugas Anda</p>
      </header>

      <!-- Toolbar: filter, sort, actions -->
      <div class="bg-white rounded-lg shadow-sm p-4 mb-4">
        <TodoFilters
          v-model:search="filters.search"
          v-model:status="filters.status"
          v-model:priority="filters.priority"
          v-model:sortBy="filters.sort_by"
          v-model:sortOrder="filters.sort_order"
          @change="onFilterChange"
        />
        <div class="flex flex-wrap gap-2 mt-4 border-t pt-4">
          <button
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition text-sm font-medium"
            @click="openCreateForm"
          >
            + Tambah Todo
          </button>
          <button
            class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="seeding"
            @click="handleSeed"
          >
            {{ seeding ? 'Menambahkan 1000 data...' : 'Seed 1000 Data Acak' }}
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div v-if="loading" class="p-10 text-center text-gray-400 text-sm">Memuat data...</div>
        <div v-else-if="todos.length === 0" class="p-10 text-center text-gray-400 text-sm">
          Tidak ada data todo yang cocok.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm text-left">
            <thead class="bg-gray-100 text-gray-600 text-xs">
              <tr>
                <th class="px-4 py-3 font-medium">Title</th>
                <th class="px-4 py-3 font-medium">Status</th>
                <th class="px-4 py-3 font-medium">Priority</th>
                <th class="px-4 py-3 font-medium">Diperbarui</th>
                <th class="px-4 py-3 font-medium text-right">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="todo in todos" :key="todo.id" class="hover:bg-gray-50">
                <td class="px-4 py-3">
                  <div class="font-medium text-gray-800">{{ todo.title }}</div>
                  <div v-if="todo.description" class="text-gray-400 text-xs mt-0.5 line-clamp-1">
                    {{ todo.description }}
                  </div>
                </td>
                <td class="px-4 py-3">
                  <span class="px-2 py-1 rounded-full text-xs font-medium" :class="statusClass(todo.status)">
                    {{ statusLabel(todo.status) }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <span class="px-2 py-1 rounded-full text-xs font-medium" :class="priorityClass(todo.priority)">
                    {{ priorityLabel(todo.priority) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-gray-500 whitespace-nowrap">{{ formatDate(todo.updated_at) }}</td>
                <td class="px-4 py-3 text-right whitespace-nowrap">
                  <button
                    class="text-blue-600 hover:text-blue-800 mr-3 text-xs font-medium"
                    @click="openEditForm(todo)"
                  >
                    Edit
                  </button>
                  <button
                    class="text-red-600 hover:text-red-800 text-xs font-medium"
                    @click="confirmDelete(todo)"
                  >
                    Hapus
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <Pagination
        v-if="!loading && todos.length > 0"
        :page="pagination.page"
        :total-pages="pagination.total_pages"
        :total="pagination.total"
        :page-size="pagination.page_size"
        @change-page="onChangePage"
      />
    </div>

    <TodoForm v-if="showForm" :todo="editingTodo" @close="showForm = false" @saved="onSaved" />

    <ConfirmModal
      v-if="deletingTodo"
      title="Hapus Todo"
      :message="`Apakah Anda yakin ingin menghapus '${deletingTodo.title}'?`"
      @cancel="deletingTodo = null"
      @confirm="handleDelete"
    />

    <Toast v-if="toast.show" :type="toast.type" :message="toast.message" @close="toast.show = false" />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import api from './api'
import ConfirmModal from './components/ConfirmModal.vue'
import Pagination from './components/Pagination.vue'
import Toast from './components/Toast.vue'
import TodoFilters from './components/TodoFilters.vue'
import TodoForm from './components/TodoForm.vue'

const todos = ref([])
const loading = ref(false)
const seeding = ref(false)
const showForm = ref(false)
const editingTodo = ref(null)
const deletingTodo = ref(null)

const filters = reactive({
  search: '',
  status: '',
  priority: '',
  sort_by: 'created_at',
  sort_order: 'desc',
})

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0,
  total_pages: 0,
})

const toast = reactive({ show: false, type: 'success', message: '' })

function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

let searchDebounce = null

function onFilterChange() {
  clearTimeout(searchDebounce)
  searchDebounce = setTimeout(() => {
    pagination.page = 1
    fetchTodos()
  }, 300)
}

async function fetchTodos() {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      sort_by: filters.sort_by,
      sort_order: filters.sort_order,
    }
    if (filters.search) params.search = filters.search
    if (filters.status) params.status = filters.status
    if (filters.priority) params.priority = filters.priority

    const { data } = await api.getTodos(params)
    todos.value = data.data
    pagination.total = data.total
    pagination.total_pages = data.total_pages
    pagination.page = data.page
    pagination.page_size = data.page_size
  } catch (err) {
    showToast(extractError(err), 'error')
  } finally {
    loading.value = false
  }
}

function onChangePage(newPage) {
  pagination.page = newPage
  fetchTodos()
}

function openCreateForm() {
  editingTodo.value = null
  showForm.value = true
}

function openEditForm(todo) {
  editingTodo.value = { ...todo }
  showForm.value = true
}

function onSaved(message) {
  showForm.value = false
  showToast(message)
  fetchTodos()
}

function confirmDelete(todo) {
  deletingTodo.value = todo
}

async function handleDelete() {
  try {
    await api.deleteTodo(deletingTodo.value.id)
    showToast('Todo berhasil dihapus')
    if (todos.value.length === 1 && pagination.page > 1) {
      pagination.page -= 1
    }
    deletingTodo.value = null
    fetchTodos()
  } catch (err) {
    showToast(extractError(err), 'error')
    deletingTodo.value = null
  }
}

async function handleSeed() {
  seeding.value = true
  try {
    const { data } = await api.seedTodos(1000)
    showToast(data.message)
    pagination.page = 1
    fetchTodos()
  } catch (err) {
    showToast(extractError(err), 'error')
  } finally {
    seeding.value = false
  }
}

function extractError(err) {
  const detail = err?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => d.msg || JSON.stringify(d)).join(', ')
  return 'Terjadi kesalahan, silakan coba lagi.'
}

function statusLabel(status) {
  return { pending: 'Pending', progress: 'Progress', done: 'Done' }[status] || status
}
function priorityLabel(priority) {
  return { low: 'Low', medium: 'Medium', high: 'High' }[priority] || priority
}
function statusClass(status) {
  return {
    pending: 'bg-gray-100 text-gray-600',
    progress: 'bg-amber-100 text-amber-700',
    done: 'bg-emerald-100 text-emerald-700',
  }[status]
}
function priorityClass(priority) {
  return {
    low: 'bg-sky-100 text-sky-700',
    medium: 'bg-indigo-100 text-indigo-700',
    high: 'bg-rose-100 text-rose-700',
  }[priority]
}
function formatDate(value) {
  if (!value) return '-'
  return new Date(value).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

onMounted(fetchTodos)
</script>
