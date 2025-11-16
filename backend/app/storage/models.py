from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Boolean

from app.storage.database import Base


class MetricSampleDB(Base):
    __tablename__ = "metric_samples"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    disk_io = Column(Float)
    slow_queries = Column(Integer)
    blocking_sessions = Column(Integer)
    deadlocks = Column(Integer)
    job_failures = Column(Integer)


class AlertDB(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    message = Column(String)
    severity = Column(String)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
