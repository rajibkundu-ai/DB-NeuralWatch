const ReplicaRow = ({ replica }) => (
  <div className="replica-card">
    <div className="replica-header">
      <div>
        <h4>{replica.name}</h4>
        <p className="muted">{replica.role}</p>
      </div>
      <span className={`chip ${replica.health}`}>{replica.health}</span>
    </div>
    <div className="replica-stats">
      <div>
        <span>Log send queue</span>
        <strong>{replica.log_send_queue_mb} MB</strong>
      </div>
      <div>
        <span>Redo queue</span>
        <strong>{replica.redo_queue_mb} MB</strong>
      </div>
      <div>
        <span>Latency</span>
        <strong>{replica.latency_ms} ms</strong>
      </div>
    </div>
    <p className="muted">{replica.synchronization_state}</p>
  </div>
)

const AgMonitoringPanel = ({ replicas = [] }) => {
  if (!replicas?.length) return null
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>AG monitoring</h2>
      </div>
      <div className="replica-grid">
        {replicas.map((replica) => (
          <ReplicaRow key={replica.name} replica={replica} />
        ))}
      </div>
    </section>
  )
}

export default AgMonitoringPanel
