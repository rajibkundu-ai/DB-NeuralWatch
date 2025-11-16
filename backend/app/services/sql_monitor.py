from __future__ import annotations

import random
from datetime import datetime
from typing import Dict, Any

try:  # Optional dependency
    import pyodbc  # type: ignore
except Exception:  # pragma: no cover - optional import fallback
    pyodbc = None

from app.core.config import get_settings
from app.models.schemas import MetricSample


METRIC_QUERY = """
SELECT
    (SELECT TOP 1 total_cpu_usage_percent FROM sys.dm_os_performance_counters) AS cpu_percent,
    (SELECT TOP 1 total_physical_memory_kb FROM sys.dm_os_sys_memory) AS total_memory,
    (SELECT TOP 1 available_physical_memory_kb FROM sys.dm_os_sys_memory) AS available_memory,
    (SELECT COUNT(*) FROM sys.dm_exec_requests WHERE total_elapsed_time > 5000) AS slow_queries,
    (SELECT COUNT(*) FROM sys.dm_os_waiting_tasks WHERE blocking_session_id IS NOT NULL) AS blocking_sessions,
    (SELECT COUNT(*) FROM sys.dm_os_ring_buffers WHERE ring_buffer_type = 'RING_BUFFER_DEADLOCK') AS deadlocks
"""


class SQLServerMonitor:
    """Collects metrics from SQL Server using DMVs. Falls back to simulated data when unavailable."""

    def __init__(self) -> None:
        settings = get_settings()
        self.connection_string = settings.sqlserver_connection_string

    def _simulate_metrics(self) -> MetricSample:
        base = random.uniform(20, 40)
        sample = MetricSample(
            cpu_percent=min(100.0, base + random.uniform(-5, 35)),
            memory_percent=min(100.0, base + random.uniform(-5, 40)),
            disk_io=random.uniform(30, 120),
            slow_queries=random.randint(0, 10),
            blocking_sessions=random.randint(0, 4),
            deadlocks=random.randint(0, 2),
            job_failures=random.randint(0, 1),
        )
        return sample

    def collect_metrics(self) -> MetricSample:
        if not self.connection_string or pyodbc is None:
            return self._simulate_metrics()

        try:
            conn = pyodbc.connect(self.connection_string, timeout=3)
            cursor = conn.cursor()
            cursor.execute(METRIC_QUERY)
            row = cursor.fetchone()
            if not row:
                raise RuntimeError("No data returned from SQL Server")
            total_memory = row.total_memory or 1
            available_memory = row.available_memory or 0
            memory_percent = (1 - (available_memory / total_memory)) * 100
            sample = MetricSample(
                cpu_percent=float(row.cpu_percent or 0),
                memory_percent=memory_percent,
                disk_io=random.uniform(20, 150),  # Placeholder until custom query implemented
                slow_queries=int(row.slow_queries or 0),
                blocking_sessions=int(row.blocking_sessions or 0),
                deadlocks=int(row.deadlocks or 0),
                job_failures=0,
            )
            cursor.close()
            conn.close()
            return sample
        except Exception:
            return self._simulate_metrics()
