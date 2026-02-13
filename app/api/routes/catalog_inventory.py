from fastapi import APIRouter

from app.schemas.catalog import Product, ProductBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/catalog/inventory", tags=["catalog-inventory"])


@router.get("", response_model=list[Product])
async def list_inventory() -> list[Product]:
    return []


@router.post("", response_model=Product)
async def create_inventory_item(payload: ProductBase) -> Product:
    product = Product(id="product_1", **payload.model_dump())
    await publish_event(RealtimeEvent(topic="inventory.updated", payload=product.model_dump()))
    return product


@router.get("/{item_id}", response_model=Product)
async def get_inventory_item(item_id: str) -> Product:
    return Product(id=item_id, name="", units=0, price=0.0, description="")


@router.post("/{item_id}/discount")
async def discount_inventory_item(item_id: str, discount: float) -> dict[str, str]:
    await publish_event(RealtimeEvent(topic="inventory.updated", payload={"id": item_id, "discount": discount}))
    return {"status": "queued"}
