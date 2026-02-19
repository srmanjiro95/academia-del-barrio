from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.core.ws import DEFAULT_TOPICS, ws_manager
from app.db.session import SessionLocal
from app.models.entities import GymMemberModel, ProductModel, PromotionModel
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
    await _send_initial_snapshots(websocket)
    try:
        while True:
            message: Any = await websocket.receive_json()
            if isinstance(message, dict) and message.get("action") == "subscribe":
                topics = [str(t) for t in message.get("topics", []) if isinstance(t, str)]
                ws_manager.set_subscriptions(websocket, topics or list(DEFAULT_TOPICS))
                await websocket.send_json({"topic": "system", "payload": {"subscribed": topics or list(DEFAULT_TOPICS)}})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


async def _send_initial_snapshots(websocket: WebSocket) -> None:
    async with SessionLocal() as session:
        inventory = [
            {"id": p.id, "name": p.name, "units": p.units, "price": p.price, "description": p.description}
            for p in (await session.execute(select(ProductModel))).scalars().all()
        ]
        promotions = [
            {
                "id": p.id,
                "title": p.title,
                "type": p.type,
                "discountType": p.discount_type,
                "amount": p.amount,
                "description": p.description,
                "startDate": p.start_date,
                "endDate": p.end_date,
                "code": p.code,
                "status": p.status,
                "imageUrl": p.image_url,
            }
            for p in (await session.execute(select(PromotionModel))).scalars().all()
        ]
        members = [
            {
                "id": m.id,
                "firstName": m.first_name,
                "lastName": m.last_name,
                "middleName": m.middle_name,
                "email": m.email,
                "phone": m.phone,
                "address": m.address,
                "status": m.status,
                "membershipId": m.membership_id,
                "membershipName": m.membership_name,
                "membershipStartDate": m.membership_start_date,
                "membershipEndDate": m.membership_end_date,
                "membershipPrice": m.membership_price,
                "qrUuid": m.qr_uuid,
                "qrImageUrl": m.qr_image_url,
                "imageUrl": m.image_url,
            }
            for m in (await session.execute(select(GymMemberModel))).scalars().all()
        ]

    await websocket.send_json({"topic": "inventory.updated", "payload": inventory})
    await websocket.send_json({"topic": "promotions.updated", "payload": promotions})
    await websocket.send_json({"topic": "members.updated", "payload": members})
