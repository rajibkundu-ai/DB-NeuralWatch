const Header = ({ onLogout, connectionInfo }) => (
  <header className="app-header">
    <div>
      <p className="brand-pill">NextGenMas</p>
      <h1>DB NeuralWatch</h1>
      <p>NextGenMas-crafted intelligence for SQL Server performance</p>
      {connectionInfo && (
        <p className="connection-meta">
          Host: <strong>{connectionInfo.host || 'Unknown'}</strong> · Database{' '}
          <strong>{connectionInfo.database || 'Unknown'}</strong>
        </p>
      )}
    </div>
    <button className="ghost" onClick={onLogout}>Logout</button>
  </header>
)

export default Header
