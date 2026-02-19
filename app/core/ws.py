from collections import defaultdict
from typing import Any

from fastapi import WebSocket

DEFAULT_TOPICS = {"inventory.updated", "promotions.updated", "members.updated"}


class WebSocketManager:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._subscriptions: dict[WebSocket, set[str]] = defaultdict(set)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)
        self._subscriptions[websocket] = set(DEFAULT_TOPICS)

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.discard(websocket)
        self._subscriptions.pop(websocket, None)

    def set_subscriptions(self, websocket: WebSocket, topics: list[str]) -> None:
        self._subscriptions[websocket] = set(topics)

    async def broadcast(self, message: dict[str, Any]) -> None:
        topic = str(message.get("topic", ""))
        stale: list[WebSocket] = []
        for connection in self._connections:
            if topic and topic not in self._subscriptions.get(connection, set()):
                continue
            try:
                await connection.send_json(message)
            except RuntimeError:
                stale.append(connection)
        for connection in stale:
            self.disconnect(connection)


ws_manager = WebSocketManager()
