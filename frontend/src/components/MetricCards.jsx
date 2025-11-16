const MetricCard = ({ label, value, suffix = '', trend }) => (
  <div className="metric-card">
    <p>{label}</p>
    <h3>
      {value}
      {suffix}
    </h3>
    {trend && <span className={`trend ${trend.type}`}>{trend.text}</span>}
  </div>
)

const MetricCards = ({ metrics }) => {
  if (!metrics) return null
  return (
    <div className="grid metrics">
      <MetricCard label="CPU" value={metrics.cpu_percent?.toFixed(1)} suffix="%" />
      <MetricCard label="Memory" value={metrics.memory_percent?.toFixed(1)} suffix="%" />
      <MetricCard label="Disk I/O" value={metrics.disk_io?.toFixed(1)} suffix=" MB/s" />
      <MetricCard label="Slow queries" value={metrics.slow_queries} />
      <MetricCard label="Blocking sessions" value={metrics.blocking_sessions} />
      <MetricCard label="Deadlocks" value={metrics.deadlocks} />
      <MetricCard label="Job failures" value={metrics.job_failures} />
    </div>
  )
}

export default MetricCards
