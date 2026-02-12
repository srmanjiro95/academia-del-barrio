from fastapi import APIRouter

from app.schemas.gym import Sale, SaleBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/gym/sales", tags=["gym-sales"])


@router.get("", response_model=list[Sale])
async def list_sales() -> list[Sale]:
    return []


@router.post("", response_model=Sale)
async def create_sale(payload: SaleBase) -> Sale:
    sale = Sale(id="sale_1", **payload.model_dump())
    await publish_event(RealtimeEvent(topic="inventory.updated", payload={"sale": sale.model_dump()}))
    return sale


@router.get("/{sale_id}", response_model=Sale)
async def get_sale(sale_id: str) -> Sale:
    return Sale(id=sale_id, customer="", product_id="", product="", quantity=0, total=0.0, date="")
