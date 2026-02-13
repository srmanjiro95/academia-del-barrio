from fastapi import APIRouter

from app.schemas.admin import Role, RoleBase

router = APIRouter(prefix="/admin/roles", tags=["admin-roles"])


@router.get("", response_model=list[Role])
async def list_roles() -> list[Role]:
    return []


@router.post("", response_model=Role)
async def create_role(payload: RoleBase) -> Role:
    return Role(id="role_1", name=payload.name, permission_ids=payload.permission_ids, permissions=[])


@router.get("/{role_id}", response_model=Role)
async def get_role(role_id: str) -> Role:
    return Role(id=role_id, name="", permission_ids=[], permissions=[])
