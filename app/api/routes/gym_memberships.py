from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import MemberMembershipModel
from app.schemas.gym import MemberMembership, MemberMembershipBase

router = APIRouter(prefix="/gym/memberships", tags=["gym-memberships"])


@router.get("", response_model=list[MemberMembership])
async def list_gym_memberships(db: AsyncSession = Depends(get_db)) -> list[MemberMembership]:
    rows = (await db.execute(select(MemberMembershipModel))).scalars().all()
    return [MemberMembership(**_to_dict(row)) for row in rows]


@router.post("", response_model=MemberMembership)
async def create_gym_membership(payload: MemberMembershipBase, db: AsyncSession = Depends(get_db)) -> MemberMembership:
    model = MemberMembershipModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return MemberMembership(**_to_dict(model))


@router.get("/{membership_id}", response_model=MemberMembership)
async def get_gym_membership(membership_id: str, db: AsyncSession = Depends(get_db)) -> MemberMembership:
    model = await db.get(MemberMembershipModel, membership_id)
    if not model:
        raise HTTPException(status_code=404, detail="Member membership not found")
    return MemberMembership(**_to_dict(model))


def _to_dict(model: MemberMembershipModel) -> dict:
    return {
        "id": model.id,
        "member_id": model.member_id,
        "member_name": model.member_name,
        "membership_id": model.membership_id,
        "membership_name": model.membership_name,
        "start_date": model.start_date,
        "end_date": model.end_date,
        "status": model.status,
    }
