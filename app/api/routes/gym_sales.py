from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import SaleModel
from app.schemas.gym import Sale, SaleBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event

router = APIRouter(prefix="/gym/sales", tags=["gym-sales"])


@router.get("", response_model=list[Sale])
async def list_sales(db: AsyncSession = Depends(get_db)) -> list[Sale]:
    rows = (await db.execute(select(SaleModel))).scalars().all()
    return [Sale(**_to_dict(row)) for row in rows]


@router.post("", response_model=Sale)
async def create_sale(payload: SaleBase, db: AsyncSession = Depends(get_db)) -> Sale:
    model = SaleModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)

    sale = Sale(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="inventory.updated", payload={"sale": sale.model_dump()}))
    return sale


@router.put("/{sale_id}", response_model=Sale)
async def update_sale(sale_id: str, payload: SaleBase, db: AsyncSession = Depends(get_db)) -> Sale:
    model = await db.get(SaleModel, sale_id)
    if not model:
        raise HTTPException(status_code=404, detail="Sale not found")

    for key, value in payload.model_dump().items():
        setattr(model, key, value)

    await db.commit()
    await db.refresh(model)

    sale = Sale(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="inventory.updated", payload={"sale": sale.model_dump()}))
    return sale


@router.get("/{sale_id}", response_model=Sale)
async def get_sale(sale_id: str, db: AsyncSession = Depends(get_db)) -> Sale:
    model = await db.get(SaleModel, sale_id)
    if not model:
        raise HTTPException(status_code=404, detail="Sale not found")
    return Sale(**_to_dict(model))


def _to_dict(model: SaleModel) -> dict:
    return {
        "id": model.id,
        "customer": model.customer,
        "product_id": model.product_id,
        "product": model.product,
        "quantity": model.quantity,
        "total": model.total,
        "date": model.date,
    }
