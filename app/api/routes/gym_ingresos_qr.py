from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import CheckInModel, GymMemberModel, PersonalRecordModel
from app.schemas.gym import (
    CheckIn,
    CheckInBase,
    CheckInByQRRequest,
    FightRecord,
    FightRecordSummary,
    MemberScannerCard,
    QRScanResponse,
)
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/gym/ingresos-qr", tags=["gym-ingresos-qr"])


@router.get("", response_model=list[CheckIn])
async def list_qr_entries(db: AsyncSession = Depends(get_db)) -> list[CheckIn]:
    rows = (await db.execute(select(CheckInModel))).scalars().all()
    return [CheckIn(**_to_checkin_dict(row)) for row in rows]


@router.post("", response_model=QRScanResponse)
async def create_qr_entry(payload: CheckInByQRRequest, db: AsyncSession = Depends(get_db)) -> QRScanResponse:
    member = (
        await db.execute(select(GymMemberModel).where(GymMemberModel.qr_uuid == payload.qr_uuid))
    ).scalars().first()
    if not member:
        raise HTTPException(status_code=404, detail="Member with qr_uuid not found")

    member_name = f"{member.first_name} {member.last_name} {member.middle_name}".strip()
    checkin_status = "Aceptado" if member.status == "Activo" else "Rechazado"
    checkin_date = datetime.utcnow().isoformat()

    model = CheckInModel(
        id=uuid4().hex,
        member_id=member.id,
        member_name=member_name,
        date=checkin_date,
        status=checkin_status,
    )
    db.add(model)
    await db.commit()
    await db.refresh(model)

    checkin = CheckIn(**_to_checkin_dict(model))

    records = (
        await db.execute(select(PersonalRecordModel).where(PersonalRecordModel.member_id == member.id))
    ).scalars().all()
    fight_records = [
        FightRecord(
            id=record.id,
            category=record.category,
            wins=record.wins,
            losses=record.losses,
            draws=record.draws,
            wins_by_ko=record.wins_by_ko,
            wins_by_points=record.wins_by_points,
        )
        for record in records
    ]

    summary = FightRecordSummary(
        total_wins=sum(r.wins for r in fight_records),
        total_losses=sum(r.losses for r in fight_records),
        total_draws=sum(r.draws for r in fight_records),
        total_wins_by_ko=sum(r.wins_by_ko for r in fight_records),
        total_wins_by_points=sum(r.wins_by_points for r in fight_records),
    )

    member_card = MemberScannerCard(
        id=member.id,
        full_name=member_name,
        status=member.status,
        membership_name=member.membership_name,
        membership_end_date=member.membership_end_date,
        image_url=member.image_url,
    )

    response = QRScanResponse(
        checkin=checkin,
        member=member_card,
        fight_records=fight_records,
        fight_summary=summary,
    )

    await publish_event(RealtimeEvent(topic="members.updated", payload={"checkin": checkin.model_dump()}))
    return response


@router.put("/{entry_id}", response_model=CheckIn)
async def update_qr_entry(entry_id: str, payload: CheckInBase, db: AsyncSession = Depends(get_db)) -> CheckIn:
    model = await db.get(CheckInModel, entry_id)
    if not model:
        raise HTTPException(status_code=404, detail="Check-in not found")

    model.member_id = payload.member_id
    model.member_name = payload.member_name
    model.date = payload.date
    model.status = payload.status

    await db.commit()
    await db.refresh(model)

    checkin = CheckIn(**_to_checkin_dict(model))
    await publish_event(RealtimeEvent(topic="members.updated", payload={"checkin": checkin.model_dump()}))
    return checkin

@router.get("/{entry_id}", response_model=CheckIn)
async def get_qr_entry(entry_id: str, db: AsyncSession = Depends(get_db)) -> CheckIn:
    model = await db.get(CheckInModel, entry_id)
    if not model:
        raise HTTPException(status_code=404, detail="Check-in not found")
    return CheckIn(**_to_checkin_dict(model))


def _to_checkin_dict(model: CheckInModel) -> dict:
    return {
        "id": model.id,
        "member_id": model.member_id,
        "member_name": model.member_name,
        "date": model.date,
        "status": model.status,
    }
