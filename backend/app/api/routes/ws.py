import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.utils.security import get_current_user
from app.workers.collector import collector

router = APIRouter(tags=["ws"])


@router.websocket("/ws/metrics")
async def metrics_ws(websocket: WebSocket):
    await websocket.accept()

    async def push(sample):
        await websocket.send_text(json.dumps(sample.model_dump(), default=str))

    collector.subscribe(push)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        return
