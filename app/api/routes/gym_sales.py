from datetime import datetime

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
    event = RealtimeEvent(topic="gym.sale", payload=sale.model_dump())
    await publish_event(event)
    return sale


@router.get("/{sale_id}", response_model=Sale)
async def get_sale(sale_id: str) -> Sale:
    now = datetime.utcnow()
    return Sale(id=sale_id, member_id=None, total=0.0, created_at=now)
