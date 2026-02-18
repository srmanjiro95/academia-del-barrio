from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import PermissionModel
from app.schemas.admin import PermissionCreate, Permissions

router = APIRouter(prefix="/admin/permissions", tags=["admin-permissions"])


@router.get("", response_model=list[Permissions])
async def list_permissions(db: AsyncSession = Depends(get_db)) -> list[Permissions]:
    rows = (await db.execute(select(PermissionModel))).scalars().all()
    return [Permissions(id=row.id, name=row.name) for row in rows]


@router.post("", response_model=Permissions)
async def create_permission(payload: PermissionCreate, db: AsyncSession = Depends(get_db)) -> Permissions:
    model = PermissionModel(id=uuid4().hex, name=payload.name)
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return Permissions(id=model.id, name=model.name)


@router.put("/{permission_id}", response_model=Permissions)
async def update_permission(permission_id: str, payload: PermissionCreate, db: AsyncSession = Depends(get_db)) -> Permissions:
    model = await db.get(PermissionModel, permission_id)
    if not model:
        raise HTTPException(status_code=404, detail="Permission not found")
    model.name = payload.name
    await db.commit()
    await db.refresh(model)
    return Permissions(id=model.id, name=model.name)


@router.get("/{permission_id}", response_model=Permissions)
async def get_permission(permission_id: str, db: AsyncSession = Depends(get_db)) -> Permissions:
    model = await db.get(PermissionModel, permission_id)
    if not model:
        raise HTTPException(status_code=404, detail="Permission not found")
    return Permissions(id=model.id, name=model.name)
