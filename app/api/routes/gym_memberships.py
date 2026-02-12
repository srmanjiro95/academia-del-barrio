from fastapi import APIRouter

from app.schemas.gym import MemberMembership, MemberMembershipBase

router = APIRouter(prefix="/gym/memberships", tags=["gym-memberships"])


@router.get("", response_model=list[MemberMembership])
async def list_gym_memberships() -> list[MemberMembership]:
    return []


@router.post("", response_model=MemberMembership)
async def create_gym_membership(payload: MemberMembershipBase) -> MemberMembership:
    return MemberMembership(id="gmem_1", **payload.model_dump())


@router.get("/{membership_id}", response_model=MemberMembership)
async def get_gym_membership(membership_id: str) -> MemberMembership:
    return MemberMembership(
        id=membership_id,
        member_id="",
        member_name="",
        membership_id="",
        membership_name="",
        start_date="",
        end_date="",
        status="Vigente",
    )
