from fastapi import APIRouter

from app.schemas.catalog import CatalogMembership, CatalogMembershipBase

router = APIRouter(prefix="/catalog/memberships", tags=["catalog-memberships"])


@router.get("", response_model=list[CatalogMembership])
async def list_catalog_memberships() -> list[CatalogMembership]:
    return []


@router.post("", response_model=CatalogMembership)
async def create_catalog_membership(payload: CatalogMembershipBase) -> CatalogMembership:
    return CatalogMembership(id="catmem_1", **payload.model_dump())


@router.get("/{membership_id}", response_model=CatalogMembership)
async def get_catalog_membership(membership_id: str) -> CatalogMembership:
    return CatalogMembership(id=membership_id, name="", duration_days=0, price=0.0)
