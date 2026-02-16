from fastapi import APIRouter

from app.schemas.catalog import Promotion, PromotionBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/catalog/promotions", tags=["catalog-promotions"])


@router.get("", response_model=list[Promotion])
async def list_promotions() -> list[Promotion]:
    return []


@router.post("", response_model=Promotion)
async def create_promotion(payload: PromotionBase) -> Promotion:
    promotion = Promotion(id="promo_1", **payload.model_dump())
    await publish_event(RealtimeEvent(topic="promotions.updated", payload=promotion.model_dump()))
    return promotion


@router.get("/{promotion_id}", response_model=Promotion)
async def get_promotion(promotion_id: str) -> Promotion:
    return Promotion(
        id=promotion_id,
        title="",
        type="Descuento",
        discount_type="Porcentaje",
        amount=0,
        description="",
        start_date="",
        end_date="",
        code="",
        status="Inactivo",
        image_url="",
    )
