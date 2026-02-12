from fastapi import APIRouter

from app.schemas.catalog import Promotion, PromotionBase

router = APIRouter(prefix="/catalog/promotions", tags=["catalog-promotions"])


@router.get("", response_model=list[Promotion])
async def list_promotions() -> list[Promotion]:
    return []


@router.post("", response_model=Promotion)
async def create_promotion(payload: PromotionBase) -> Promotion:
    return Promotion(id="promo_1", **payload.model_dump())


@router.get("/{promotion_id}", response_model=Promotion)
async def get_promotion(promotion_id: str) -> Promotion:
    return Promotion(id=promotion_id, name="", description=None, discount_percent=None)
