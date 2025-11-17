import axios from 'axios'

const buildApiBaseUrl = () => {
  const envBaseUrl = import.meta.env.VITE_API_BASE_URL
  const fallbackBaseUrl = `${window.location.origin}/api`

  const configuredBaseUrl = envBaseUrl && envBaseUrl.trim() !== ''
    ? envBaseUrl
    : fallbackBaseUrl

  const normalizedBaseUrl = configuredBaseUrl.replace(/\/$/, '')
  const apiBase = normalizedBaseUrl.endsWith('/api')
    ? normalizedBaseUrl
    : `${normalizedBaseUrl}/api`

  const apiUrl = new URL(apiBase)
  const pageProtocol = window.location.protocol

  if (pageProtocol === 'https:' && apiUrl.protocol === 'http:' && apiUrl.hostname === window.location.hostname) {
    apiUrl.protocol = 'https:'
  }

  if (apiUrl.hostname !== window.location.hostname) {
    console.warn(`API base URL host ("${apiUrl.hostname}") differs from page host ("${window.location.hostname}").`)
  }

  return apiUrl.toString().replace(/\/$/, '')
}

const apiBaseUrl = buildApiBaseUrl()

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
