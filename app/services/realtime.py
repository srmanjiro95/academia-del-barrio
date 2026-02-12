import asyncio
import json
from typing import Any

from redis.asyncio.client import PubSub

from app.core.redis import redis_client
from app.core.ws import ws_manager
from app.schemas.realtime import RealtimeEvent

CHANNEL_NAME = "realtime-events"


async def publish_event(event: RealtimeEvent) -> None:
    await redis_client.publish(CHANNEL_NAME, event.model_dump_json())


async def start_listener(stop_event: asyncio.Event) -> None:
    pubsub: PubSub = redis_client.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)
    try:
        async for message in pubsub.listen():
            if stop_event.is_set():
                break
            if message["type"] != "message":
                continue
            raw_data = message["data"]
            payload = _parse_payload(raw_data)
            await ws_manager.broadcast(payload)
    finally:
        await pubsub.unsubscribe(CHANNEL_NAME)
        await pubsub.close()


def _parse_payload(raw_data: Any) -> dict[str, Any]:
    if isinstance(raw_data, bytes):
        raw_data = raw_data.decode("utf-8")
    if isinstance(raw_data, str):
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError:
            return {"topic": CHANNEL_NAME, "payload": raw_data}
    if isinstance(raw_data, dict):
        return raw_data
    return {"topic": CHANNEL_NAME, "payload": raw_data}
