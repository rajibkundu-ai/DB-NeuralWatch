# SQL Server Performance Monitoring Web App

A fully fledged, containerized web application designed to monitor SQL Server database performance in real time.
It provides modern, responsive dashboards, alerting, authentication, and historical reporting — all configurable via .env.

## 🚀 Features

### 📊 Real-Time Dashboards
- CPU & memory usage
- Disk I/O performance
- Slow queries
- Blocking sessions
- Deadlocks
- Long-running queries
- SQL Agent job failures
- Query performance trends

### 🔔 Alerting System
Configurable thresholds for:
- High CPU/memory
- Long-running queries
- Blocking/deadlocks
- Disk pressure
- Failed jobs

Alerts can be delivered via:
- Email
- Slack / Teams (optional)
- Web notifications

### 📈 Historical Reporting
Stores long-term data for analysis and capacity planning.

### 🔐 Authentication
- Login credentials stored in .env
- Optional JWT-based session authentication
- Optional role-based access control

### 📱 Modern & Mobile Friendly
- Responsive UI
- Dashboard-oriented layout
- Mobile-first design

### 🐳 Fully Containerized
Runs entirely in Docker with configuration provided via environment variables.

## 📦 Project Structure


/project-root
 ├── backend/               # API + data collectors
 ├── frontend/              # Modern web UI
 ├── docker-compose.yml
 ├── Dockerfile
 ├── .env.example
 └── README.md


## ⚙ Requirements

- Docker + Docker Compose
- Accessible SQL Server instance
- .env file with required variables

## 🔧 Environment Variables

Create a .env file in the project root:


# Database Connection
DB_HOST=your-sql-host
DB_PORT=1433
DB_USER=sa
DB_PASSWORD=yourpassword
DB_NAME=master

# App Credentials
APP_USERNAME=admin
APP_PASSWORD=yourStrongPassword

# Alerts
ALERT_EMAIL_ENABLED=true
ALERT_EMAIL_TO=admin@example.com
ALERT_THRESHOLD_CPU=85
ALERT_THRESHOLD_QUERY_TIME_MS=2000

# JWT / Session Security
JWT_SECRET=yourjwtsecret

# Optional Integrations
SLACK_WEBHOOK_URL=
TEAMS_WEBHOOK_URL=


> Never commit your real .env file. Use .env.example instead.

## ▶ Running the App (Docker)


docker-compose up --build


Access the app at:


http://localhost:8080


Log in using credentials from .env.

## 🛠 Development Setup

### Backend


cd backend
npm install
npm run dev


### Frontend


cd frontend
npm install
npm run dev


## 📡 Data Collection

Performance data is collected using SQL Server DMVs, including:

- sys.dm_exec_query_stats
- sys.dm_os_performance_counters
- sys.dm_exec_requests
- sys.dm_exec_sessions
- sys.dm_os_wait_stats
- sys.dm_db_index_usage_stats

## 📬 Alerting Logic

Alerts are triggered when:

- CPU or memory exceed thresholds
- Queries exceed expected duration
- Blocking occurs
- SQL Agent jobs fail
- Deadlocks are detected

## 🔐 Security

- All sensitive values stored in environment variables
- No secrets exposed to the frontend
- HTTPS strongly recommended in production

## 🌐 Deployment

Supports deployment on:

- Docker Swarm
- Kubernetes
- AWS ECS
- Any container orchestration platform

## 📄 License

MIT License (or your own choice)
