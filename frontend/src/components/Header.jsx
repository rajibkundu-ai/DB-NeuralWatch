const Header = ({ onLogout }) => (
  <header className="app-header">
    <div>
      <h1>DB NeuralWatch</h1>
      <p>SQL Server performance intelligence</p>
    </div>
    <button className="ghost" onClick={onLogout}>Logout</button>
  </header>
)

export default Header
