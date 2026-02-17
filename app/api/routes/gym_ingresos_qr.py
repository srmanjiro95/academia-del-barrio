from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import CheckInModel
from app.schemas.gym import CheckIn, CheckInBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/gym/ingresos-qr", tags=["gym-ingresos-qr"])


@router.get("", response_model=list[CheckIn])
async def list_qr_entries(db: AsyncSession = Depends(get_db)) -> list[CheckIn]:
    rows = (await db.execute(select(CheckInModel))).scalars().all()
    return [CheckIn(**_to_dict(row)) for row in rows]


@router.post("", response_model=CheckIn)
async def create_qr_entry(payload: CheckInBase, db: AsyncSession = Depends(get_db)) -> CheckIn:
    model = CheckInModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)

    checkin = CheckIn(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="members.updated", payload={"checkin": checkin.model_dump()}))
    return checkin


@router.get("/{entry_id}", response_model=CheckIn)
async def get_qr_entry(entry_id: str, db: AsyncSession = Depends(get_db)) -> CheckIn:
    model = await db.get(CheckInModel, entry_id)
    if not model:
        raise HTTPException(status_code=404, detail="Check-in not found")
    return CheckIn(**_to_dict(model))


def _to_dict(model: CheckInModel) -> dict:
    return {
        "id": model.id,
        "member_id": model.member_id,
        "member_name": model.member_name,
        "date": model.date,
        "status": model.status,
    }
