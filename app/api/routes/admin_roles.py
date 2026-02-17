from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import PermissionModel, RoleModel, role_permissions
from app.schemas.admin import Permissions, Role, RoleBase

router = APIRouter(prefix="/admin/roles", tags=["admin-roles"])


@router.get("", response_model=list[Role])
async def list_roles(db: AsyncSession = Depends(get_db)) -> list[Role]:
    roles = (await db.execute(select(RoleModel))).scalars().all()
    return [await _build_role_response(db, role) for role in roles]


@router.post("", response_model=Role)
async def create_role(payload: RoleBase, db: AsyncSession = Depends(get_db)) -> Role:
    role = RoleModel(id=uuid4().hex, name=payload.name)
    db.add(role)
    await db.flush()

    for permission_id in payload.permission_ids:
        await db.execute(insert(role_permissions).values(role_id=role.id, permission_id=permission_id))

    await db.commit()
    await db.refresh(role)
    return await _build_role_response(db, role)


@router.get("/{role_id}", response_model=Role)
async def get_role(role_id: str, db: AsyncSession = Depends(get_db)) -> Role:
    role = await db.get(RoleModel, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return await _build_role_response(db, role)


async def _build_role_response(db: AsyncSession, role: RoleModel) -> Role:
    rows = (
        await db.execute(
            select(PermissionModel)
            .join(role_permissions, PermissionModel.id == role_permissions.c.permission_id)
            .where(role_permissions.c.role_id == role.id)
        )
    ).scalars().all()

    permissions = [Permissions(id=p.id, name=p.name) for p in rows]
    permission_ids = [p.id for p in rows]
    return Role(id=role.id, name=role.name, permission_ids=permission_ids, permissions=permissions)
