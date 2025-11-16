import { useState } from 'react'
import { login as loginApi } from '../api/client'

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(Boolean(localStorage.getItem('dbnw_token')))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const login = async (username, password) => {
    setLoading(true)
    setError('')
    try {
      await loginApi(username, password)
      setIsAuthenticated(true)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to login')
      setIsAuthenticated(false)
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('dbnw_token')
    setIsAuthenticated(false)
  }

  return { isAuthenticated, login, logout, loading, error }
}
