import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
})

export default {
  getTodos(params) {
    return api.get('/api/todos', { params })
  },
  getTodo(id) {
    return api.get(`/api/todos/${id}`)
  },
  createTodo(data) {
    return api.post('/api/todos', data)
  },
  updateTodo(id, data) {
    return api.put(`/api/todos/${id}`, data)
  },
  deleteTodo(id) {
    return api.delete(`/api/todos/${id}`)
  },
  seedTodos(count) {
    return api.post('/api/todos/seed', { count })
  },
}
