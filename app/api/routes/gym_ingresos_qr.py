from fastapi import APIRouter

from app.schemas.gym import CheckIn, CheckInBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/gym/ingresos-qr", tags=["gym-ingresos-qr"])


@router.get("", response_model=list[CheckIn])
async def list_qr_entries() -> list[CheckIn]:
    return []


@router.post("", response_model=CheckIn)
async def create_qr_entry(payload: CheckInBase) -> CheckIn:
    checkin = CheckIn(id="checkin_1", **payload.model_dump())
    await publish_event(RealtimeEvent(topic="members.updated", payload={"checkin": checkin.model_dump()}))
    return checkin


@router.get("/{entry_id}", response_model=CheckIn)
async def get_qr_entry(entry_id: str) -> CheckIn:
    return CheckIn(id=entry_id, member_id="", member_name="", date="", status="Rechazado")
