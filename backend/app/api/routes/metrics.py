from fastapi import APIRouter, Depends

from app.models.schemas import HistoricalQuery, TrendResponse
from app.storage import repository
from app.utils.security import get_current_user

router = APIRouter(prefix="/metrics", tags=["metrics"], dependencies=[Depends(get_current_user)])


@router.get("/latest")
def latest_metrics():
    samples = repository.get_latest_metrics(limit=1)
    return samples[0] if samples else {}


@router.get("/history")
def history(hours: int = 24):
    return repository.get_metrics_since(hours)


@router.get("/alerts")
def active_alerts():
    return repository.get_active_alerts()


@router.post("/trends", response_model=TrendResponse)
def trends(payload: HistoricalQuery):
    points = repository.trend_data(payload.hours)
    return TrendResponse(points=points)
