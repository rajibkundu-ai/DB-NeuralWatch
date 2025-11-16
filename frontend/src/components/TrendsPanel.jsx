const TrendTile = ({ label, value, suffix }) => (
  <div className="trend-tile">
    <p>{label}</p>
    <h4>
      {value}
      {suffix}
    </h4>
  </div>
)

const TrendsPanel = ({ data = [] }) => (
  <section className="panel">
    <div className="panel-header">
      <h2>Hourly trends</h2>
    </div>
    <div className="grid trends">
      {data.map((point) => (
        <TrendTile
          key={point.bucket}
          label={new Date(point.bucket).toLocaleString([], { hour: '2-digit', minute: '2-digit' })}
          value={point.cpu_avg?.toFixed(1)}
          suffix="% avg CPU"
        />
      ))}
    </div>
  </section>
)

export default TrendsPanel
