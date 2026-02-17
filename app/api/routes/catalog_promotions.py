from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import PromotionModel
from app.schemas.catalog import Promotion, PromotionBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/catalog/promotions", tags=["catalog-promotions"])


@router.get("", response_model=list[Promotion])
async def list_promotions(db: AsyncSession = Depends(get_db)) -> list[Promotion]:
    rows = (await db.execute(select(PromotionModel))).scalars().all()
    return [Promotion(**_to_dict(row)) for row in rows]


@router.post("", response_model=Promotion)
async def create_promotion(payload: PromotionBase, db: AsyncSession = Depends(get_db)) -> Promotion:
    model = PromotionModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)

    promotion = Promotion(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="promotions.updated", payload=promotion.model_dump()))
    return promotion


@router.get("/{promotion_id}", response_model=Promotion)
async def get_promotion(promotion_id: str, db: AsyncSession = Depends(get_db)) -> Promotion:
    model = await db.get(PromotionModel, promotion_id)
    if not model:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return Promotion(**_to_dict(model))


def _to_dict(model: PromotionModel) -> dict:
    return {
        "id": model.id,
        "title": model.title,
        "type": model.type,
        "discount_type": model.discount_type,
        "amount": model.amount,
        "description": model.description,
        "start_date": model.start_date,
        "end_date": model.end_date,
        "code": model.code,
        "status": model.status,
        "image_url": model.image_url,
    }
