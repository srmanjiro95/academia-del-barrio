from pydantic import BaseModel, EmailStr


class EmergencyContact(BaseModel):
    name: str
    phone: str
    relationship: str


class Permissions(BaseModel):
    id: str
    name: str


class PermissionCreate(BaseModel):
    name: str


class RoleBase(BaseModel):
    name: str
    permission_ids: list[str] = []


class Role(RoleBase):
    id: str
    permissions: list[Permissions] = []


class InternalUserBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    email: EmailStr
    phone: str
    address: str
    role_id: str | None = None
    role: str | None = None
    emergency_contacts: list[EmergencyContact] = []
    image_url: str | None = None


class InternalUser(InternalUserBase):
    id: str


class PersonalRecordBase(BaseModel):
    member_id: str
    member_name: str
    category: str
    wins: int
    losses: int
    draws: int
    wins_by_ko: int
    wins_by_points: int
    image_url: str | None = None


class PersonalRecord(PersonalRecordBase):
    id: str
