const AlertsPanel = ({ alerts = [] }) => (
  <section className="panel">
    <div className="panel-header">
      <h2>Active alerts</h2>
      <span>{alerts.length}</span>
    </div>
    <div className="alert-list">
      {alerts.length === 0 && <p className="muted">No alerts 🎉</p>}
      {alerts.map((alert) => (
        <article key={alert.id} className={`alert ${alert.severity}`}>
          <h4>{alert.message}</h4>
          <small>{new Date(alert.created_at).toLocaleString()}</small>
        </article>
      ))}
    </div>
  </section>
)

export default AlertsPanel
