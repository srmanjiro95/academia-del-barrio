from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    units: int
    price: float
    description: str
    image_url: str | None = None


class Product(ProductBase):
    id: str


class MembershipBase(BaseModel):
    name: str
    price: float
    duration: str
    includes: list[str] = []
    image_url: str | None = None


class Membership(MembershipBase):
    id: str


class PromotionBase(BaseModel):
    title: str
    type: str
    discount_type: str | None = None
    amount: float
    description: str
    start_date: str
    end_date: str
    code: str
    status: str
    image_url: str


class Promotion(PromotionBase):
    id: str


class DevelopmentPlanBase(BaseModel):
    name: str
    description: str
    member_id: str
    member_name: str
    focus: str
    coach: str
    sessions_per_week: int


class DevelopmentPlan(DevelopmentPlanBase):
    id: str
