from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import ProductModel
from app.schemas.catalog import Product, ProductBase
from app.schemas.realtime import RealtimeEvent
from app.services.realtime import publish_event
from app.services.storage import absolute_media_url, save_upload_file

router = APIRouter(prefix="/catalog/inventory", tags=["catalog-inventory"])


@router.get("", response_model=list[Product])
async def list_inventory(db: AsyncSession = Depends(get_db)) -> list[Product]:
    rows = (await db.execute(select(ProductModel))).scalars().all()
    return [Product(**_to_dict(row)) for row in rows]


@router.post("", response_model=Product)
async def create_inventory_item(payload: ProductBase, db: AsyncSession = Depends(get_db)) -> Product:
    model = ProductModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)

    product = Product(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="inventory.updated", payload=product.model_dump()))
    return product


@router.put("/{item_id}", response_model=Product)
async def update_inventory_item(item_id: str, payload: ProductBase, db: AsyncSession = Depends(get_db)) -> Product:
    model = await db.get(ProductModel, item_id)
    if not model:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in payload.model_dump().items():
        setattr(model, key, value)

    await db.commit()
    await db.refresh(model)

    product = Product(**_to_dict(model))
    await publish_event(RealtimeEvent(topic="inventory.updated", payload=product.model_dump()))
    return product


@router.get("/{item_id}", response_model=Product)
async def get_inventory_item(item_id: str, db: AsyncSession = Depends(get_db)) -> Product:
    model = await db.get(ProductModel, item_id)
    if not model:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**_to_dict(model))


@router.post("/{item_id}/discount")
async def discount_inventory_item(item_id: str, discount: float, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    model = await db.get(ProductModel, item_id)
    if not model:
        raise HTTPException(status_code=404, detail="Product not found")

    model.price = max(0.0, model.price - discount)
    await db.commit()
    await db.refresh(model)

    await publish_event(RealtimeEvent(topic="inventory.updated", payload=_to_dict(model)))
    return {"status": "queued"}


@router.post("/{item_id}/image", response_model=Product)
async def upload_inventory_image(
    item_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> Product:
    model = await db.get(ProductModel, item_id)
    if not model:
        raise HTTPException(status_code=404, detail="Product not found")

    model.image_url = absolute_media_url(await save_upload_file(file, "inventory"))
    await db.commit()
    await db.refresh(model)
    return Product(**_to_dict(model))


def _to_dict(model: ProductModel) -> dict:
    return {
        "id": model.id,
        "name": model.name,
        "category": model.category,
        "units": model.units,
        "price": model.price,
        "description": model.description,
        "image_url": model.image_url,
    }
