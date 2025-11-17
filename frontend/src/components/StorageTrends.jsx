const StorageTile = ({ item }) => (
  <div className="storage-card">
    <p>{item.label}</p>
    <h3>
      {item.value}
      <span className="unit"> {item.unit}</span>
    </h3>
    <span className={`chip subtle ${item.direction}`}>{item.direction}</span>
    <p className="muted small">{item.description}</p>
  </div>
)

const StorageTrends = ({ data = [] }) => {
  if (!data?.length) return null
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Storage trends</h2>
      </div>
      <div className="storage-grid">
        {data.map((item) => (
          <StorageTile key={item.label} item={item} />
        ))}
      </div>
    </section>
  )
}

export default StorageTrends
