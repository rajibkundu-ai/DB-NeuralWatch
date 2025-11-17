from fastapi import APIRouter, Depends, HTTPException

from app.core.config import get_settings
from app.models.schemas import InsightResponse, QueryPerformance, RealtimePerformance
from app.services.ag_monitor import AGMonitor
from app.storage import repository
from app.utils.connection import extract_connection_details
from app.utils.security import get_current_user

router = APIRouter(prefix="/metadata", tags=["metadata"], dependencies=[Depends(get_current_user)])

settings = get_settings()
ag_monitor = AGMonitor()


@router.get("/connection")
def connection_info():
    host, database = extract_connection_details(settings.sqlserver_connection_string)
    return {
        "app": settings.app_name,
        "host": host,
        "database": database,
    }


def _query_status(sample: RealtimePerformance) -> QueryPerformance:
    score = (
        sample.slow_queries
        + (sample.blocking_sessions * 2)
        + (sample.deadlocks * 3)
        + (sample.job_failures * 4)
    )
    if score >= 12:
        status = "critical"
        message = "Immediate attention required. Deadlocks or job failures detected."
    elif score >= 4:
        status = "watch"
        message = "Query delays detected. Review blocking sessions and slow queries."
    else:
        status = "healthy"
        message = "Queries are completing within expected thresholds."
    return QueryPerformance(
        status=status,
        message=message,
        slow_queries=sample.slow_queries,
        blocking_sessions=sample.blocking_sessions,
        deadlocks=sample.deadlocks,
        job_failures=sample.job_failures,
    )


@router.get("/insights", response_model=InsightResponse)
def operational_insights() -> InsightResponse:
    samples = repository.get_latest_metrics(limit=1)
    if not samples:
        raise HTTPException(status_code=404, detail="No metrics available")
    latest = samples[0]
    realtime = RealtimePerformance(
        cpu_percent=latest.cpu_percent,
        memory_percent=latest.memory_percent,
        disk_io=latest.disk_io,
        slow_queries=latest.slow_queries,
        blocking_sessions=latest.blocking_sessions,
        deadlocks=latest.deadlocks,
        job_failures=latest.job_failures,
        updated_at=latest.timestamp,
    )

    query = _query_status(realtime)
    ag = ag_monitor.current_status()
    storage = repository.storage_trend_summary()

    return InsightResponse(realtime=realtime, query=query, ag=ag, storage=storage)
