import axios from 'axios'

// On Vercel (production), VITE_API_BASE is empty -> relative to same origin
// In local dev, set VITE_API_BASE=http://127.0.0.1:8000 in .env.local
const API_BASE = (import.meta.env.VITE_API_BASE ?? '')

const api = axios.create({ baseURL: API_BASE })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (r) => r,
  (err) => {
    err.message = err?.response?.data?.detail || err.message || 'Request failed'
    return Promise.reject(err)
  }
)

export async function login(username, password) {
  const { data } = await api.post('/api/auth/login', { username, password })
  localStorage.setItem('token', data.access)
  return data
}

export async function register(payload) {
  return api.post('/api/auth/register', payload)
}

export async function listMyShops(params = {}) {
  const { data } = await api.get('/api/shops/', { params })
  return data
}

export async function createShop(payload) {
  const { data } = await api.post('/api/shops/', payload)
  return data
}

export async function deleteShop(id) {
  await api.delete(`/api/shops/${id}/`)
}

export async function nearby(lat, lng, radius = 5) {
  const { data } = await api.get('/api/shops/nearby/', { params: { lat, lng, radius } })
  return data
}

export async function geocodeCity(city) {
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(city)}&limit=1`
  const res = await fetch(url, { headers: { 'Accept-Language': 'en' } })
  const data = await res.json()
  if (!Array.isArray(data) || data.length === 0) throw new Error('City not found')
  const first = data[0]
  return { lat: parseFloat(first.lat), lng: parseFloat(first.lon) }
}

export default api