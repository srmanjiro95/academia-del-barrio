from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: str | None = None


class Role(RoleBase):
    id: str


class PermissionBase(BaseModel):
    code: str
    description: str | None = None


class Permission(PermissionBase):
    id: str


class InternalUserBase(BaseModel):
    email: str
    full_name: str
    role_id: str | None = None


class InternalUser(InternalUserBase):
    id: str


class PersonalRecordBase(BaseModel):
    employee_id: str
    notes: str | None = None


class PersonalRecord(PersonalRecordBase):
    id: str
