from sqlalchemy import Column, Float, ForeignKey, Integer, JSON, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String(64), ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", String(64), ForeignKey("permissions.id"), primary_key=True),
)


class PermissionModel(Base):
    __tablename__ = "permissions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class RoleModel(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)


class InternalUserModel(Base):
    __tablename__ = "internal_users"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[str | None] = mapped_column(ForeignKey("roles.id"), nullable=True)
    role: Mapped[str | None] = mapped_column(String(80), nullable=True)
    emergency_contacts: Mapped[list[dict]] = mapped_column(JSON, default=list)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)


class ProductModel(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    units: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    price: Mapped[float] = mapped_column(Float(), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)


class MembershipModel(Base):
    __tablename__ = "memberships"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float(), nullable=False)
    duration: Mapped[str] = mapped_column(String(40), nullable=False)
    includes: Mapped[list[str]] = mapped_column(JSON, default=list)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)


class PromotionModel(Base):
    __tablename__ = "promotions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    discount_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    amount: Mapped[float] = mapped_column(Float(), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    start_date: Mapped[str] = mapped_column(String(30), nullable=False)
    end_date: Mapped[str] = mapped_column(String(30), nullable=False)
    code: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)


class GymMemberModel(Base):
    __tablename__ = "gym_members"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    email: Mapped[str] = mapped_column(String(180), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[str | None] = mapped_column(String(30), nullable=True)
    health: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    guardian: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    emergency_contacts: Mapped[list[dict]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    membership_id: Mapped[str | None] = mapped_column(ForeignKey("memberships.id"), nullable=True)
    membership_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    membership_start_date: Mapped[str | None] = mapped_column(String(30), nullable=True)
    membership_end_date: Mapped[str | None] = mapped_column(String(30), nullable=True)
    membership_price: Mapped[float | None] = mapped_column(Float(), nullable=True)
    qr_uuid: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    qr_image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)


class MemberMembershipModel(Base):
    __tablename__ = "member_memberships"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    member_id: Mapped[str | None] = mapped_column(ForeignKey("gym_members.id"), nullable=True)
    member_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    membership_id: Mapped[str] = mapped_column(ForeignKey("memberships.id"), nullable=False)
    membership_name: Mapped[str] = mapped_column(String(120), nullable=False)
    start_date: Mapped[str] = mapped_column(String(30), nullable=False)
    end_date: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)


class CheckInModel(Base):
    __tablename__ = "checkins"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    member_id: Mapped[str | None] = mapped_column(ForeignKey("gym_members.id"), nullable=True)
    member_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    date: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)


class DevelopmentPlanModel(Base):
    __tablename__ = "development_plans"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    member_id: Mapped[str | None] = mapped_column(ForeignKey("gym_members.id"), nullable=True)
    member_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    focus: Mapped[str] = mapped_column(String(120), nullable=False)
    coach: Mapped[str] = mapped_column(String(120), nullable=False)
    sessions_per_week: Mapped[int] = mapped_column(Integer(), nullable=False)


class PersonalRecordModel(Base):
    __tablename__ = "personal_records"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    member_id: Mapped[str | None] = mapped_column(ForeignKey("gym_members.id"), nullable=True)
    member_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    wins: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    losses: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    draws: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    wins_by_ko: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    wins_by_points: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)


class SaleModel(Base):
    __tablename__ = "sales"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    customer: Mapped[str] = mapped_column(String(180), nullable=False)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False)
    product: Mapped[str] = mapped_column(String(150), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer(), nullable=False)
    total: Mapped[float] = mapped_column(Float(), nullable=False)
    date: Mapped[str] = mapped_column(String(30), nullable=False)
