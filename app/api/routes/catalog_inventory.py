from fastapi import APIRouter

from app.schemas.catalog import InventoryItem, InventoryItemBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/catalog/inventory", tags=["catalog-inventory"])


@router.get("", response_model=list[InventoryItem])
async def list_inventory() -> list[InventoryItem]:
    return []


@router.post("", response_model=InventoryItem)
async def create_inventory_item(payload: InventoryItemBase) -> InventoryItem:
    return InventoryItem(id="item_1", **payload.model_dump())


@router.get("/{item_id}", response_model=InventoryItem)
async def get_inventory_item(item_id: str) -> InventoryItem:
    return InventoryItem(id=item_id, name="", sku="", quantity=0, price=None)


@router.post("/{item_id}/discount")
async def discount_inventory_item(item_id: str, payload: InventoryItemBase) -> dict[str, str]:
    event = RealtimeEvent(topic="inventory.discount", payload={"item_id": item_id, **payload.model_dump()})
    await publish_event(event)
    return {"status": "queued"}
