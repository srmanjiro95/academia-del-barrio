from datetime import datetime

from pydantic import BaseModel


class GymMembershipBase(BaseModel):
    member_id: str
    plan_id: str
    start_date: datetime
    end_date: datetime


class GymMembership(GymMembershipBase):
    id: str


class GymMemberBase(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None


class GymMember(GymMemberBase):
    id: str


class QrEntryBase(BaseModel):
    member_id: str
    scanned_at: datetime


class QrEntry(QrEntryBase):
    id: str


class SaleBase(BaseModel):
    member_id: str | None = None
    total: float
    created_at: datetime


class Sale(SaleBase):
    id: str
