from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MetricSample(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    cpu_percent: float
    memory_percent: float
    disk_io: float
    slow_queries: int
    blocking_sessions: int
    deadlocks: int
    job_failures: int


class Alert(BaseModel):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    message: str
    severity: str
    resolved: bool = False
    resolved_at: Optional[datetime] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HistoricalQuery(BaseModel):
    hours: int = 24


class TrendPoint(BaseModel):
    bucket: datetime
    cpu_avg: float
    memory_avg: float
    disk_io_avg: float


class TrendResponse(BaseModel):
    points: List[TrendPoint]
