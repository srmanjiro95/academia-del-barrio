import asyncio
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.ws import ws_manager
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(tags=["realtime"])


@router.post("/events")
async def post_event(event: RealtimeEvent) -> dict[str, str]:
    await publish_event(event)
    return {"status": "queued"}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await ws_manager.connect(websocket)
    try:
        while True:
            message: Any = await websocket.receive_json()
            if isinstance(message, dict):
                await ws_manager.broadcast({"topic": "client", "payload": message})
            await asyncio.sleep(0)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
