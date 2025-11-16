import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, metrics, ws
from app.core.config import get_settings
from app.workers.collector import collector

app = FastAPI(title="DB NeuralWatch", version="1.0.0")

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
    ,
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(metrics.router)
app.include_router(ws.router)


@app.on_event("startup")
async def startup_event() -> None:
    await collector.start()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await collector.stop()


@app.get("/")
def read_root():
    return {"message": "DB NeuralWatch API", "app": settings.app_name}
