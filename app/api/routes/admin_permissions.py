from fastapi import APIRouter

from app.schemas.admin import Permission, PermissionBase

router = APIRouter(prefix="/admin/permissions", tags=["admin-permissions"])


@router.get("", response_model=list[Permission])
async def list_permissions() -> list[Permission]:
    return []


@router.post("", response_model=Permission)
async def create_permission(payload: PermissionBase) -> Permission:
    return Permission(id="perm_1", **payload.model_dump())


@router.get("/{permission_id}", response_model=Permission)
async def get_permission(permission_id: str) -> Permission:
    return Permission(id=permission_id, code="", description=None)
