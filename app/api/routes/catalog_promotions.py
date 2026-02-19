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
    data = _normalize_and_validate(payload)
    model = PromotionModel(id=uuid4().hex, **data)
    db.add(model)
    await db.commit()
    await db.refresh(model)

    promotion = Promotion(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="promotions.updated", payload=promotion.model_dump()))
    return promotion


@router.put("/{promotion_id}", response_model=Promotion)
async def update_promotion(promotion_id: str, payload: PromotionBase, db: AsyncSession = Depends(get_db)) -> Promotion:
    model = await db.get(PromotionModel, promotion_id)
    if not model:
        raise HTTPException(status_code=404, detail="Promotion not found")

    for key, value in _normalize_and_validate(payload).items():
        setattr(model, key, value)

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


def _normalize_and_validate(payload: PromotionBase) -> dict:
    data = payload.model_dump()
    promotion_type = (data.get("type") or "").strip().lower()

    applies_to = (data.get("applies_to") or "all_store").strip().lower().replace(" ", "_")
    data["applies_to"] = applies_to

    if promotion_type in {"inscripción", "inscripcion"}:
        data["applies_to"] = "all_store"
        data["target_category"] = None
        data["target_product_ids"] = []
        data["target_membership_ids"] = []
        return data

    if applies_to == "all_store":
        data["target_category"] = None
        data["target_product_ids"] = []
        data["target_membership_ids"] = []
    elif applies_to == "category":
        if not data.get("target_category"):
            raise HTTPException(status_code=422, detail="target_category is required when applies_to=category")
        data["target_product_ids"] = []
        data["target_membership_ids"] = []
    elif applies_to == "products":
        if not data.get("target_product_ids"):
            raise HTTPException(status_code=422, detail="target_product_ids is required when applies_to=products")
        data["target_category"] = None
        data["target_membership_ids"] = []
    elif applies_to == "membership":
        if not data.get("target_membership_ids"):
            raise HTTPException(status_code=422, detail="target_membership_ids is required when applies_to=membership")
        data["target_category"] = None
        data["target_product_ids"] = []
    else:
        raise HTTPException(status_code=422, detail="applies_to must be one of: all_store, category, products, membership")

    return data


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
        "applies_to": model.applies_to,
        "target_category": model.target_category,
        "target_product_ids": model.target_product_ids,
        "target_membership_ids": model.target_membership_ids,
    }
