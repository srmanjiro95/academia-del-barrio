from datetime import datetime

from fastapi import APIRouter

from app.schemas.gym import QrEntry, QrEntryBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/gym/ingresos-qr", tags=["gym-ingresos-qr"])


@router.get("", response_model=list[QrEntry])
async def list_qr_entries() -> list[QrEntry]:
    return []


@router.post("", response_model=QrEntry)
async def create_qr_entry(payload: QrEntryBase) -> QrEntry:
    entry = QrEntry(id="qr_1", **payload.model_dump())
    event = RealtimeEvent(topic="gym.qr-entry", payload=entry.model_dump())
    await publish_event(event)
    return entry


@router.get("/{entry_id}", response_model=QrEntry)
async def get_qr_entry(entry_id: str) -> QrEntry:
    now = datetime.utcnow()
    return QrEntry(id=entry_id, member_id="", scanned_at=now)
