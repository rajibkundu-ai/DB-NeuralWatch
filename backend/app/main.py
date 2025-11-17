import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, metrics, metadata, ws
from app.core.config import get_settings
from app.workers.collector import collector

app = FastAPI(title="DB NeuralWatch", version="1.0.0")

settings = get_settings()

cors_origins = settings.cors_allowed_origins or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(metadata.router, prefix="/api")
app.include_router(ws.router, prefix="/api")


@app.on_event("startup")
async def startup_event() -> None:
    await collector.start()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await collector.stop()


@app.get("/")
def read_root():
    return {
        "message": "DB NeuralWatch API",
        "app": settings.app_name,
        "backend_api_url": settings.backend_api_url,
        "cors_allowed_origins": cors_origins,
    }
