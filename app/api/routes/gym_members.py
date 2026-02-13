from fastapi import APIRouter

from app.schemas.gym import GymMember, GymMemberBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/gym/members", tags=["gym-members"])


@router.get("", response_model=list[GymMember])
async def list_members() -> list[GymMember]:
    return []


@router.post("", response_model=GymMember)
async def create_member(payload: GymMemberBase) -> GymMember:
    member = GymMember(id="member_1", **payload.model_dump())
    await publish_event(RealtimeEvent(topic="members.updated", payload=member.model_dump()))
    return member


@router.get("/{member_id}", response_model=GymMember)
async def get_member(member_id: str) -> GymMember:
    return GymMember(
        id=member_id,
        first_name="",
        last_name="",
        middle_name="",
        email="test@example.com",
        phone="",
        address="",
        birth_date=None,
        health=None,
        guardian=None,
        emergency_contacts=[],
        status="Activo",
        membership_id=None,
        membership_name=None,
    )
