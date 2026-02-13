from fastapi import APIRouter

from app.schemas.catalog import Membership, MembershipBase

router = APIRouter(prefix="/catalog/memberships", tags=["catalog-memberships"])


@router.get("", response_model=list[Membership])
async def list_catalog_memberships() -> list[Membership]:
    return []


@router.post("", response_model=Membership)
async def create_catalog_membership(payload: MembershipBase) -> Membership:
    return Membership(id="membership_1", **payload.model_dump())


@router.get("/{membership_id}", response_model=Membership)
async def get_catalog_membership(membership_id: str) -> Membership:
    return Membership(id=membership_id, name="", price=0.0, duration="", includes=[])
