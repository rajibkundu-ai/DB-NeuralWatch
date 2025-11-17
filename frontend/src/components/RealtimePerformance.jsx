const StatGauge = ({ label, value, suffix }) => (
  <div className="stat-gauge">
    <p>{label}</p>
    <h3>
      {value}
      {suffix}
    </h3>
  </div>
)

const QueryStat = ({ label, value }) => (
  <div className="query-stat">
    <span>{label}</span>
    <strong>{value}</strong>
  </div>
)

const RealtimePerformance = ({ data }) => {
  if (!data?.realtime) return null
  const { realtime, query } = data
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Real-time server &amp; query performance</h2>
        {query && <span className={`chip ${query.status}`}>{query.status}</span>}
      </div>
      <div className="performance-grid">
        <div className="gauge-grid">
          <StatGauge label="CPU utilization" value={realtime.cpu_percent?.toFixed(1)} suffix="%" />
          <StatGauge label="Memory usage" value={realtime.memory_percent?.toFixed(1)} suffix="%" />
          <StatGauge label="Disk throughput" value={realtime.disk_io?.toFixed(1)} suffix=" MB/s" />
        </div>
        <div className="query-stack">
          <h3>Query health</h3>
          <p className="muted">{query?.message}</p>
          <div className="query-grid">
            <QueryStat label="Slow queries" value={realtime.slow_queries} />
            <QueryStat label="Blocking sessions" value={realtime.blocking_sessions} />
            <QueryStat label="Deadlocks" value={realtime.deadlocks} />
            <QueryStat label="Job failures" value={realtime.job_failures} />
          </div>
        </div>
      </div>
    </section>
  )
}

export default RealtimePerformance
