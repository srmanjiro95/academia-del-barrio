from datetime import datetime

from fastapi import APIRouter

from app.schemas.gym import GymMembership, GymMembershipBase

router = APIRouter(prefix="/gym/memberships", tags=["gym-memberships"])


@router.get("", response_model=list[GymMembership])
async def list_gym_memberships() -> list[GymMembership]:
    return []


@router.post("", response_model=GymMembership)
async def create_gym_membership(payload: GymMembershipBase) -> GymMembership:
    return GymMembership(id="gmem_1", **payload.model_dump())


@router.get("/{membership_id}", response_model=GymMembership)
async def get_gym_membership(membership_id: str) -> GymMembership:
    now = datetime.utcnow()
    return GymMembership(
        id=membership_id,
        member_id="",
        plan_id="",
        start_date=now,
        end_date=now,
    )
