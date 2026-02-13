from fastapi import APIRouter

from app.schemas.admin import PermissionCreate, Permissions

router = APIRouter(prefix="/admin/permissions", tags=["admin-permissions"])


@router.get("", response_model=list[Permissions])
async def list_permissions() -> list[Permissions]:
    return []


@router.post("", response_model=Permissions)
async def create_permission(payload: PermissionCreate) -> Permissions:
    return Permissions(id="perm_1", name=payload.name)


@router.get("/{permission_id}", response_model=Permissions)
async def get_permission(permission_id: str) -> Permissions:
    return Permissions(id=permission_id, name="")
