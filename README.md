# DB NeuralWatch

DB NeuralWatch is a fully containerized SQL Server performance monitoring platform. It includes a FastAPI backend that polls SQL Server DMVs, stores historical samples in SQLite, evaluates alert thresholds, and publishes real-time metrics over WebSockets. A modern Vite/React dashboard visualizes key KPIs, alerts, and long-term trends with a mobile-friendly layout.

## Features

- **Responsive dashboard** with KPI tiles, alert feeds, trend widgets, and interactive charts.
- **Credential-based authentication** using JWT, with credentials stored in `.env`.
- **SQL Server data collector** that polls CPU, memory, disk I/O, blocking, deadlocks, job failures, and slow query counts.
- **Alerting engine** with configurable CPU/memory/disk thresholds.
- **Historical storage** in SQLite for trend and reporting queries.
- **WebSocket streaming** for near real-time updates.
- **Full Docker Compose setup** for backend + frontend services.

## Project structure

```
.
├── backend/                 # FastAPI app, collectors, SQLite models
├── frontend/                # React + Vite single-page dashboard
├── docker-compose.yml       # Multi-service runtime
├── .env.example             # Backend configuration template
├── README.md
└── ...
```

## Getting started (non-technical friendly)

### 1. Install the required software

You only need two tools installed on your computer:

1. **Git** – used to download this project. Download: <https://git-scm.com/downloads>.
2. **Docker Desktop** – used to run the backend and frontend without touching any code. Download: <https://www.docker.com/products/docker-desktop/>.

> ✅ Once Docker Desktop is installed, open it at least once so it can finish its first-time setup.

### 2. Download this project

1. Open a terminal (Command Prompt or PowerShell on Windows, Terminal on macOS/Linux).
2. Pick a folder where you would like the project to live.
3. Run:

```bash
git clone https://github.com/your-org/DB-NeuralWatch.git
cd DB-NeuralWatch
```

### 3. Create your configuration file

All secrets live in one `.env` file. Follow these steps carefully:

1. Copy the example file: `cp .env.example .env` (Windows PowerShell: `copy .env.example .env`).
2. Open `.env` in a text editor (Notepad works).
3. Replace the placeholder values:
   - `ADMIN_USERNAME` / `ADMIN_PASSWORD`: choose the login you will use for the website.
   - `SECRET_KEY`: any long random string; it is used to sign login tokens.
   - `SQLSERVER_CONNECTION_STRING`: paste the connection string for the SQL Server you want to monitor. If you are just testing, keep the default; the app will simulate metrics when the server is unreachable.
   - Keep the other defaults unless you know you need different alert thresholds.

> 🔐 Never commit or share the `.env` file—it contains credentials.

If you want the frontend to call a different API URL (rare), copy `frontend/.env.example` to `frontend/.env` and edit `VITE_API_BASE_URL`.

### 4. Start everything with Docker

1. Ensure Docker Desktop is running.
2. In the project folder, run:

```bash
docker-compose up --build
```

The first run can take a few minutes because Docker needs to download images and install dependencies.

### 5. Open the apps

- **Backend API** (useful for troubleshooting only): `http://localhost:8000/docs`
- **Frontend dashboard**: `http://localhost:5173`

Log in with the username and password you added to `.env`. After login you will see metric cards, charts, and alerts. The dashboard refreshes automatically every few seconds.

### Running locally without Docker

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Update `VITE_API_BASE_URL` in `frontend/.env` to point to your backend during local development.

## Environment variables

All sensitive values (credentials, secrets, SQL Server connection strings) must live in the `.env` file at the repository root. Example:

```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=supersecret
SECRET_KEY=change-me
SQLSERVER_CONNECTION_STRING=Driver={ODBC Driver 18 for SQL Server};Server=tcp:yourserver,1433;Database=master;Uid=sa;Pwd=Strong!Pass;Encrypt=yes;
METRICS_POLL_INTERVAL=30
ALERT_CPU_THRESHOLD=85
ALERT_MEMORY_THRESHOLD=85
ALERT_DISK_IO_THRESHOLD=80
RETENTION_HOURS=336
```

### Frontend overrides (`frontend/.env`)

```
VITE_API_BASE_URL=http://localhost:8000
```

## API overview

| Method | Endpoint              | Description                        |
| ------ | --------------------- | ---------------------------------- |
| POST   | `/auth/login`         | Authenticate and receive JWT token |
| GET    | `/metrics/latest`     | Latest KPI sample                  |
| GET    | `/metrics/history`    | Historical samples (query param `hours`) |
| GET    | `/metrics/alerts`     | Active alerts                      |
| POST   | `/metrics/trends`     | Aggregated hourly trend data       |
| WS     | `/ws/metrics`         | WebSocket stream of new samples    |

All `/metrics` routes require the bearer token returned by `/auth/login`.

## Alerting

The alert manager compares each metric sample against the thresholds defined in `.env`. Alerts are persisted to SQLite and surfaced to the frontend. Current severity levels include `warning` and `critical`.

## Notes

- When SQL Server connectivity or DMVs are unavailable, the collector gracefully falls back to simulated metrics so the UI continues to function in demo environments.
- SQLite stores a rolling window of samples (default 14 days) controlled by `RETENTION_HOURS`.
- The frontend uses Recharts for plotting and automatically polls the API every 15 seconds.

## Security

- Secrets, credentials, and SQL Server connection strings stay in `.env`.
- JWT signing uses `SECRET_KEY`; rotate regularly.
- Enable HTTPS/ingress security when deploying beyond localhost.

## License

MIT (or update to match your organization).
