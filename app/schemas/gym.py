from pydantic import BaseModel, EmailStr


class ContactInfo(BaseModel):
    name: str
    phone: str


class GuardianData(BaseModel):
    name: str | None = None
    phone: str | None = None


class HealthData(BaseModel):
    height: float | None = None
    weight: float | None = None
    bmi: float | None = None
    allergies: str | None = None
    diseases: str | None = None
    previous_injuries: str | None = None


class MembershipData(BaseModel):
    id: str
    name: str


class GymMemberBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    email: EmailStr
    phone: str
    address: str
    birth_date: str | None = None
    health: HealthData | None = None
    guardian: GuardianData | None = None
    emergency_contacts: list[ContactInfo] = []
    status: str
    membership_id: str | None = None
    membership_name: str | None = None


class GymMember(GymMemberBase):
    id: str


class MemberMembershipBase(BaseModel):
    member_id: str
    member_name: str
    membership_id: str
    membership_name: str
    start_date: str
    end_date: str
    status: str


class MemberMembership(MemberMembershipBase):
    id: str


class CheckInBase(BaseModel):
    member_id: str
    member_name: str
    date: str
    status: str


class CheckIn(CheckInBase):
    id: str


class SaleBase(BaseModel):
    customer: str
    product_id: str
    product: str
    quantity: int
    total: float
    date: str


class Sale(SaleBase):
    id: str
