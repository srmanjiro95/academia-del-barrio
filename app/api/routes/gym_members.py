import re
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import GymMemberModel, MemberMembershipModel, MembershipModel
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
    membership = await _resolve_membership(db, payload.membership_id)

    membership_name = payload.membership_name or (membership.name if membership else None)
    membership_price = payload.membership_price if payload.membership_price is not None else (membership.price if membership else None)

    start_date = payload.membership_start_date or datetime.utcnow().strftime("%Y-%m-%d")
    end_date = payload.membership_end_date or _calculate_end_date(start_date, membership.duration if membership else None)

    qr_uuid = generate_member_qr()
    qr_image_url = absolute_media_url(build_member_qr_image(qr_uuid))

    model = GymMemberModel(
        id=uuid4().hex,
        **payload.model_dump(exclude={"qr_uuid", "qr_image_url", "membership_name", "membership_price", "membership_start_date", "membership_end_date"}),
        membership_name=membership_name,
        membership_price=membership_price,
        membership_start_date=start_date,
        membership_end_date=end_date,
        qr_uuid=qr_uuid,
        qr_image_url=qr_image_url,
    )
    db.add(model)
    await db.flush()

    if model.membership_id and membership_name:
        member_membership = MemberMembershipModel(
            id=uuid4().hex,
            member_id=model.id,
            member_name=f"{model.first_name} {model.last_name} {model.middle_name}".strip(),
            membership_id=model.membership_id,
            membership_name=membership_name,
            start_date=start_date,
            end_date=end_date,
            status=_membership_status(end_date),
        )
        db.add(member_membership)

    await db.commit()
    await db.refresh(model)

    member = GymMember(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="members.updated", payload=member.model_dump()))
    send_registration_email(member)
    return member


@router.post("/{member_id}/refresh-qr", response_model=GymMember)
async def refresh_member_qr(member_id: str, db: AsyncSession = Depends(get_db)) -> GymMember:
    model = await db.get(GymMemberModel, member_id)
    if not model:
        raise HTTPException(status_code=404, detail="Member not found")

    new_uuid = generate_member_qr()
    model.qr_uuid = new_uuid
    model.qr_image_url = absolute_media_url(build_member_qr_image(new_uuid))
    await db.commit()
    await db.refresh(model)

    member = GymMember(**_to_dict(model))
    send_qr_refresh_email(member)

    await publish_event(RealtimeEvent(topic="members.updated", payload=member.model_dump()))
    return member


@router.get("/{member_id}", response_model=GymMember)
async def get_member(member_id: str, db: AsyncSession = Depends(get_db)) -> GymMember:
    model = await db.get(GymMemberModel, member_id)
    if not model:
        raise HTTPException(status_code=404, detail="Member not found")
    return GymMember(**_to_dict(model))


async def _resolve_membership(db: AsyncSession, membership_id: str | None) -> MembershipModel | None:
    if not membership_id:
        return None
    membership = await db.get(MembershipModel, membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return membership


def _calculate_end_date(start_date: str, duration: str | None) -> str:
    if not duration:
        return start_date
    match = re.search(r"(\d+)", duration)
    if not match:
        return start_date
    days = int(match.group(1))
    start = datetime.strptime(start_date, "%Y-%m-%d")
    return (start + timedelta(days=days)).strftime("%Y-%m-%d")


def _membership_status(end_date: str) -> str:
    today = datetime.utcnow().date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    if end < today:
        return "Vencida"
    if end <= today + timedelta(days=7):
        return "Por vencer"
    return "Vigente"


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
        "image_url": model.image_url,
    }
