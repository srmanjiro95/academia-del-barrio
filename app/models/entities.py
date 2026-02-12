from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PromotionModel(Base):
    __tablename__ = "promotions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    discount_percent: Mapped[float | None] = mapped_column(Float(), nullable=True)


class InventoryItemModel(Base):
    __tablename__ = "inventory_items"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    sku: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    price: Mapped[float | None] = mapped_column(Float(), nullable=True)


class CatalogMembershipModel(Base):
    __tablename__ = "catalog_memberships"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer(), nullable=False)
    price: Mapped[float] = mapped_column(Float(), nullable=False)


class PlanModel(Base):
    __tablename__ = "plans"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    price: Mapped[float] = mapped_column(Float(), nullable=False)


class RoleModel(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)


class PermissionModel(Base):
    __tablename__ = "permissions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)


class InternalUserModel(Base):
    __tablename__ = "internal_users"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(180), nullable=False)
    role_id: Mapped[str | None] = mapped_column(ForeignKey("roles.id"), nullable=True)


class PersonalRecordModel(Base):
    __tablename__ = "personal_records"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    employee_id: Mapped[str] = mapped_column(String(64), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text(), nullable=True)


class GymMemberModel(Base):
    __tablename__ = "gym_members"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(180), nullable=False)
    email: Mapped[str | None] = mapped_column(String(180), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)


class GymMembershipModel(Base):
    __tablename__ = "gym_memberships"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    member_id: Mapped[str] = mapped_column(ForeignKey("gym_members.id"), nullable=False)
    plan_id: Mapped[str] = mapped_column(ForeignKey("plans.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)


class QrEntryModel(Base):
    __tablename__ = "qr_entries"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    member_id: Mapped[str] = mapped_column(ForeignKey("gym_members.id"), nullable=False)
    scanned_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)


class SaleModel(Base):
    __tablename__ = "sales"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    member_id: Mapped[str | None] = mapped_column(ForeignKey("gym_members.id"), nullable=True)
    total: Mapped[float] = mapped_column(Float(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
