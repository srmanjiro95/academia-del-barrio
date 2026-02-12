from pydantic import BaseModel


class PromotionBase(BaseModel):
    name: str
    description: str | None = None
    discount_percent: float | None = None


class Promotion(PromotionBase):
    id: str


class InventoryItemBase(BaseModel):
    name: str
    sku: str
    quantity: int
    price: float | None = None


class InventoryItem(InventoryItemBase):
    id: str


class CatalogMembershipBase(BaseModel):
    name: str
    duration_days: int
    price: float


class CatalogMembership(CatalogMembershipBase):
    id: str


class PlanBase(BaseModel):
    name: str
    description: str | None = None
    price: float


class Plan(PlanBase):
    id: str
