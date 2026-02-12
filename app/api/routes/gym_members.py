from fastapi import APIRouter

from app.schemas.gym import GymMember, GymMemberBase

router = APIRouter(prefix="/gym/members", tags=["gym-members"])


@router.get("", response_model=list[GymMember])
async def list_members() -> list[GymMember]:
    return []


@router.post("", response_model=GymMember)
async def create_member(payload: GymMemberBase) -> GymMember:
    return GymMember(id="member_1", **payload.model_dump())


@router.get("/{member_id}", response_model=GymMember)
async def get_member(member_id: str) -> GymMember:
    return GymMember(id=member_id, full_name="", email=None, phone=None)
