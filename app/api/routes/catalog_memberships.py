from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import MembershipModel
from app.schemas.catalog import Membership, MembershipBase
from app.services.storage import save_upload_file

router = APIRouter(prefix="/catalog/memberships", tags=["catalog-memberships"])


@router.get("", response_model=list[Membership])
async def list_catalog_memberships(db: AsyncSession = Depends(get_db)) -> list[Membership]:
    rows = (await db.execute(select(MembershipModel))).scalars().all()
    return [Membership(**_to_dict(row)) for row in rows]


@router.post("", response_model=Membership)
async def create_catalog_membership(payload: MembershipBase, db: AsyncSession = Depends(get_db)) -> Membership:
    model = MembershipModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return Membership(**_to_dict(model))


@router.get("/{membership_id}", response_model=Membership)
async def get_catalog_membership(membership_id: str, db: AsyncSession = Depends(get_db)) -> Membership:
    model = await db.get(MembershipModel, membership_id)
    if not model:
        raise HTTPException(status_code=404, detail="Membership not found")
    return Membership(**_to_dict(model))


@router.post("/{membership_id}/image", response_model=Membership)
async def upload_membership_image(
    membership_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> Membership:
    model = await db.get(MembershipModel, membership_id)
    if not model:
        raise HTTPException(status_code=404, detail="Membership not found")

    model.image_url = await save_upload_file(file, "memberships")
    await db.commit()
    await db.refresh(model)
    return Membership(**_to_dict(model))


def _to_dict(model: MembershipModel) -> dict:
    return {
        "id": model.id,
        "name": model.name,
        "price": model.price,
        "duration": model.duration,
        "includes": model.includes,
        "image_url": model.image_url,
    }
