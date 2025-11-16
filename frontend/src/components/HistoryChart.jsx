import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const HistoryChart = ({ data = [] }) => {
  const formatted = data.map((item) => ({
    ...item,
    timestampLabel: new Date(item.timestamp).toLocaleTimeString()
  }))

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Performance history</h2>
      </div>
      <div style={{ width: '100%', height: 320 }}>
        <ResponsiveContainer>
          <LineChart data={formatted} margin={{ top: 5, right: 20, left: 0, bottom: 0 }}>
            <Line type="monotone" dataKey="cpu_percent" stroke="#ef4444" strokeWidth={2} name="CPU %" />
            <Line type="monotone" dataKey="memory_percent" stroke="#3b82f6" strokeWidth={2} name="Memory %" />
            <Line type="monotone" dataKey="disk_io" stroke="#10b981" strokeWidth={2} name="Disk I/O" />
            <CartesianGrid stroke="#e5e7eb" strokeDasharray="3 3" />
            <XAxis dataKey="timestampLabel" interval={Math.floor(data.length / 8)} />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default HistoryChart
