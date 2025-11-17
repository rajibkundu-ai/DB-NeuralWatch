import axios from 'axios'

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL

if (!configuredBaseUrl) {
  throw new Error('API base URL is not configured. Set VITE_API_BASE_URL in your frontend environment.')
}

const normalizedBaseUrl = configuredBaseUrl.replace(/\/$/, '')
const apiBaseUrl = normalizedBaseUrl.endsWith('/api')
  ? normalizedBaseUrl
  : `${normalizedBaseUrl}/api`

const api = axios.create({
  baseURL: apiBaseUrl
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('dbnw_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const login = async (username, password) => {
  const { data } = await api.post('/auth/login', { username, password })
  localStorage.setItem('dbnw_token', data.access_token)
  return data
}

export const fetchLatestMetrics = () => api.get('/metrics/latest').then((res) => res.data)
export const fetchHistory = (hours = 24) => api.get('/metrics/history', { params: { hours } }).then((res) => res.data)
export const fetchAlerts = () => api.get('/metrics/alerts').then((res) => res.data)
export const fetchTrends = (hours = 24) => api.post('/metrics/trends', { hours }).then((res) => res.data)
export const fetchConnectionInfo = () => api.get('/metadata/connection').then((res) => res.data)
export const fetchInsights = () => api.get('/metadata/insights').then((res) => res.data)

export default api
