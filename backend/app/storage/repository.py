from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Iterable, List

from sqlalchemy import func, select, delete

from app.models.schemas import MetricSample, Alert, TrendPoint
from app.storage.database import SessionLocal, engine, Base
from app.storage.models import MetricSampleDB, AlertDB
from app.core.config import get_settings


Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def save_metric(sample: MetricSample) -> None:
    with get_session() as session:
        db_sample = MetricSampleDB(**sample.model_dump())
        session.add(db_sample)
        session.commit()


def save_alert(alert: Alert) -> None:
    with get_session() as session:
        db_alert = AlertDB(**alert.model_dump())
        session.add(db_alert)
        session.commit()


def resolve_alert(alert_id: str) -> None:
    with get_session() as session:
        alert = session.get(AlertDB, alert_id)
        if alert:
            alert.resolved = True
            alert.resolved_at = datetime.utcnow()
            session.commit()


def get_latest_metrics(limit: int = 1) -> List[MetricSample]:
    with get_session() as session:
        results = session.execute(select(MetricSampleDB).order_by(MetricSampleDB.timestamp.desc()).limit(limit))
        samples = [MetricSample(**row[0].__dict__) for row in results]
        return samples


def get_metrics_since(hours: int) -> List[MetricSample]:
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    with get_session() as session:
        results = session.execute(
            select(MetricSampleDB).where(MetricSampleDB.timestamp >= cutoff).order_by(MetricSampleDB.timestamp)
        )
        return [MetricSample(**row[0].__dict__) for row in results]


def get_active_alerts() -> List[Alert]:
    with get_session() as session:
        results = session.execute(select(AlertDB).where(AlertDB.resolved.is_(False)).order_by(AlertDB.created_at.desc()))
        return [Alert(**row[0].__dict__) for row in results]


def cleanup_old_metrics() -> None:
    settings = get_settings()
    cutoff = datetime.utcnow() - timedelta(hours=settings.retention_hours)
    with get_session() as session:
        session.execute(delete(MetricSampleDB).where(MetricSampleDB.timestamp < cutoff))
        session.commit()


def trend_data(hours: int, bucket_minutes: int = 60) -> List[TrendPoint]:
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    with get_session() as session:
        bucket = func.strftime('%Y-%m-%d %H:00:00', MetricSampleDB.timestamp)
        stmt = (
            select(
                func.datetime(bucket).label('bucket'),
                func.avg(MetricSampleDB.cpu_percent),
                func.avg(MetricSampleDB.memory_percent),
                func.avg(MetricSampleDB.disk_io),
            )
            .where(MetricSampleDB.timestamp >= cutoff)
            .group_by('bucket')
            .order_by('bucket')
        )
        rows = session.execute(stmt).all()
        return [
            TrendPoint(bucket=datetime.fromisoformat(row[0]), cpu_avg=row[1], memory_avg=row[2], disk_io_avg=row[3])
            for row in rows
        ]
