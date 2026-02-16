from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import InternalUserModel
from app.schemas.admin import InternalUser, InternalUserBase
from app.services.storage import save_upload_file

router = APIRouter(prefix="/admin/internal-users", tags=["admin-internal-users"])


@router.get("", response_model=list[InternalUser])
async def list_internal_users(db: AsyncSession = Depends(get_db)) -> list[InternalUser]:
    rows = (await db.execute(select(InternalUserModel))).scalars().all()
    return [InternalUser(**_to_dict(row)) for row in rows]


@router.post("", response_model=InternalUser)
async def create_internal_user(payload: InternalUserBase, db: AsyncSession = Depends(get_db)) -> InternalUser:
    model = InternalUserModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return InternalUser(**_to_dict(model))


@router.get("/{user_id}", response_model=InternalUser)
async def get_internal_user(user_id: str, db: AsyncSession = Depends(get_db)) -> InternalUser:
    model = await db.get(InternalUserModel, user_id)
    if not model:
        raise HTTPException(status_code=404, detail="Internal user not found")
    return InternalUser(**_to_dict(model))


@router.post("/{user_id}/image", response_model=InternalUser)
async def upload_internal_user_image(
    user_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> InternalUser:
    model = await db.get(InternalUserModel, user_id)
    if not model:
        raise HTTPException(status_code=404, detail="Internal user not found")

    model.image_url = await save_upload_file(file, "internal-users")
    await db.commit()
    await db.refresh(model)
    return InternalUser(**_to_dict(model))


def _to_dict(model: InternalUserModel) -> dict:
    return {
        "id": model.id,
        "first_name": model.first_name,
        "last_name": model.last_name,
        "middle_name": model.middle_name,
        "email": model.email,
        "phone": model.phone,
        "address": model.address,
        "role_id": model.role_id,
        "role": model.role,
        "emergency_contacts": model.emergency_contacts,
        "image_url": model.image_url,
    }
