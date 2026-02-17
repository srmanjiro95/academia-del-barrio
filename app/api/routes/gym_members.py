from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import GymMemberModel
from app.schemas.gym import GymMember, GymMemberBase
from app.schemas.realtime import RealtimeEvent
from app.services.email import send_qr_refresh_email, send_registration_email
from app.services.qr import absolute_media_url, build_member_qr_image, generate_member_qr
from app.services.realtime import publish_event

router = APIRouter(prefix="/gym/members", tags=["gym-members"])


@router.get("", response_model=list[GymMember])
async def list_members(db: AsyncSession = Depends(get_db)) -> list[GymMember]:
    rows = (await db.execute(select(GymMemberModel))).scalars().all()
    return [GymMember(**_to_dict(row)) for row in rows]


@router.post("", response_model=GymMember)
async def create_member(payload: GymMemberBase, db: AsyncSession = Depends(get_db)) -> GymMember:
    qr_uuid = generate_member_qr()
    qr_image_url = build_member_qr_image(qr_uuid)

    model = GymMemberModel(
        id=uuid4().hex,
        **payload.model_dump(exclude={"qr_uuid", "qr_image_url"}),
        qr_uuid=qr_uuid,
        qr_image_url=qr_image_url,
    )
    db.add(model)
    await db.commit()
    await db.refresh(model)

    member = GymMember(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="members.updated", payload=member.model_dump()))

    email_member = member.model_copy(update={"qr_image_url": absolute_media_url(member.qr_image_url or "")})
    send_registration_email(email_member)
    return member


@router.post("/{member_id}/refresh-qr", response_model=GymMember)
async def refresh_member_qr(member_id: str, db: AsyncSession = Depends(get_db)) -> GymMember:
    model = await db.get(GymMemberModel, member_id)
    if not model:
        raise HTTPException(status_code=404, detail="Member not found")

    new_uuid = generate_member_qr()
    model.qr_uuid = new_uuid
    model.qr_image_url = build_member_qr_image(new_uuid)
    await db.commit()
    await db.refresh(model)

    member = GymMember(**_to_dict(model))
    email_member = member.model_copy(update={"qr_image_url": absolute_media_url(member.qr_image_url or "")})
    send_qr_refresh_email(email_member)

    await publish_event(RealtimeEvent(topic="members.updated", payload=member.model_dump()))
    return member


@router.get("/{member_id}", response_model=GymMember)
async def get_member(member_id: str, db: AsyncSession = Depends(get_db)) -> GymMember:
    model = await db.get(GymMemberModel, member_id)
    if not model:
        raise HTTPException(status_code=404, detail="Member not found")
    return GymMember(**_to_dict(model))


def _to_dict(model: GymMemberModel) -> dict:
    return {
        "id": model.id,
        "first_name": model.first_name,
        "last_name": model.last_name,
        "middle_name": model.middle_name,
        "email": model.email,
        "phone": model.phone,
        "address": model.address,
        "birth_date": model.birth_date,
        "health": model.health,
        "guardian": model.guardian,
        "emergency_contacts": model.emergency_contacts,
        "status": model.status,
        "membership_id": model.membership_id,
        "membership_name": model.membership_name,
        "membership_start_date": model.membership_start_date,
        "membership_end_date": model.membership_end_date,
        "membership_price": model.membership_price,
        "qr_uuid": model.qr_uuid,
        "qr_image_url": model.qr_image_url,
    }
