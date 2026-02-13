from fastapi import APIRouter

from app.schemas.admin import InternalUser, InternalUserBase

router = APIRouter(prefix="/admin/internal-users", tags=["admin-internal-users"])


@router.get("", response_model=list[InternalUser])
async def list_internal_users() -> list[InternalUser]:
    return []


@router.post("", response_model=InternalUser)
async def create_internal_user(payload: InternalUserBase) -> InternalUser:
    return InternalUser(id="user_1", **payload.model_dump())


@router.get("/{user_id}", response_model=InternalUser)
async def get_internal_user(user_id: str) -> InternalUser:
    return InternalUser(
        id=user_id,
        first_name="",
        last_name="",
        middle_name="",
        email="test@example.com",
        phone="",
        address="",
        role_id=None,
        role=None,
        emergency_contacts=[],
    )
