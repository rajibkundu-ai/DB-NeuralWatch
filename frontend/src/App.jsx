import { useEffect, useMemo, useState } from 'react'
import LoginForm from './components/LoginForm'
import Header from './components/Header'
import MetricCards from './components/MetricCards'
import AlertsPanel from './components/AlertsPanel'
import HistoryChart from './components/HistoryChart'
import TrendsPanel from './components/TrendsPanel'
import RealtimePerformance from './components/RealtimePerformance'
import AgMonitoringPanel from './components/AgMonitoringPanel'
import StorageTrends from './components/StorageTrends'
import { useAuth } from './hooks/useAuth'
import {
  fetchLatestMetrics,
  fetchHistory,
  fetchAlerts,
  fetchTrends,
  fetchConnectionInfo,
  fetchInsights
} from './api/client'

const App = () => {
  const { isAuthenticated, login, logout, loading, error } = useAuth()
  const [metrics, setMetrics] = useState(null)
  const [history, setHistory] = useState([])
  const [alerts, setAlerts] = useState([])
  const [trends, setTrends] = useState([])
  const [range, setRange] = useState(24)
  const [connectionInfo, setConnectionInfo] = useState(null)
  const [insights, setInsights] = useState(null)

  const loadAll = async () => {
    try {
      const [latest, historyData, alertsData, trendsData, insightsData] = await Promise.all([
        fetchLatestMetrics(),
        fetchHistory(range),
        fetchAlerts(),
        fetchTrends(range),
        fetchInsights().catch(() => null)
      ])
      setMetrics(latest)
      setHistory(historyData)
      setAlerts(alertsData)
      setTrends(trendsData.points)
      setInsights(insightsData)
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('Failed to load dashboard data', err)
    }
  }

  useEffect(() => {
    if (!isAuthenticated) return
    loadAll()
    const interval = setInterval(loadAll, 15000)
    return () => clearInterval(interval)
  }, [isAuthenticated, range])

  useEffect(() => {
    if (!isAuthenticated) {
      setConnectionInfo(null)
      return
    }
    const loadConnectionInfo = async () => {
      try {
        const info = await fetchConnectionInfo()
        setConnectionInfo(info)
      } catch (err) {
        setConnectionInfo(null)
      }
    }
    loadConnectionInfo()
  }, [isAuthenticated])

  const filteredHistory = useMemo(() => history.slice(-120), [history])

  if (!isAuthenticated) {
    return (
      <main className="auth-layout">
        <LoginForm onSubmit={login} loading={loading} error={error} />
      </main>
    )
  }

  return (
    <main className="app-shell">
      <Header onLogout={logout} connectionInfo={connectionInfo} />
      <section className="controls">
        <label>
          History range
          <select value={range} onChange={(e) => setRange(Number(e.target.value))}>
            <option value={6}>6 hours</option>
            <option value={12}>12 hours</option>
            <option value={24}>24 hours</option>
            <option value={72}>3 days</option>
          </select>
        </label>
      </section>
      <MetricCards metrics={metrics} />
      <RealtimePerformance data={insights} />
      <div className="grid layout">
        <AlertsPanel alerts={alerts} />
        <HistoryChart data={filteredHistory} />
      </div>
      <div className="grid layout">
        <AgMonitoringPanel replicas={insights?.ag} />
        <StorageTrends data={insights?.storage} />
      </div>
      <TrendsPanel data={trends} />
    </main>
  )
}

export default App
