from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import PersonalRecordModel
from app.schemas.admin import PersonalRecord, PersonalRecordBase
from app.services.storage import absolute_media_url, save_upload_file

router = APIRouter(prefix="/admin/personal-records", tags=["admin-personal-records"])


@router.get("", response_model=list[PersonalRecord])
async def list_personal_records(db: AsyncSession = Depends(get_db)) -> list[PersonalRecord]:
    rows = (await db.execute(select(PersonalRecordModel))).scalars().all()
    return [PersonalRecord(**_to_dict(row)) for row in rows]


@router.post("", response_model=PersonalRecord)
async def create_personal_record(payload: PersonalRecordBase, db: AsyncSession = Depends(get_db)) -> PersonalRecord:
    model = PersonalRecordModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return PersonalRecord(**_to_dict(model))


@router.put("/{record_id}", response_model=PersonalRecord)
async def update_personal_record(record_id: str, payload: PersonalRecordBase, db: AsyncSession = Depends(get_db)) -> PersonalRecord:
    model = await db.get(PersonalRecordModel, record_id)
    if not model:
        raise HTTPException(status_code=404, detail="Personal record not found")

    for key, value in payload.model_dump().items():
        setattr(model, key, value)

    await db.commit()
    await db.refresh(model)
    return PersonalRecord(**_to_dict(model))


@router.get("/{record_id}", response_model=PersonalRecord)
async def get_personal_record(record_id: str, db: AsyncSession = Depends(get_db)) -> PersonalRecord:
    model = await db.get(PersonalRecordModel, record_id)
    if not model:
        raise HTTPException(status_code=404, detail="Personal record not found")
    return PersonalRecord(**_to_dict(model))


@router.post("/{record_id}/image", response_model=PersonalRecord)
async def upload_personal_record_image(
    record_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> PersonalRecord:
    model = await db.get(PersonalRecordModel, record_id)
    if not model:
        raise HTTPException(status_code=404, detail="Personal record not found")

    model.image_url = absolute_media_url(await save_upload_file(file, "personal-records"))
    await db.commit()
    await db.refresh(model)
    return PersonalRecord(**_to_dict(model))


def _to_dict(model: PersonalRecordModel) -> dict:
    return {
        "id": model.id,
        "member_id": model.member_id,
        "member_name": model.member_name,
        "category": model.category,
        "wins": model.wins,
        "losses": model.losses,
        "draws": model.draws,
        "wins_by_ko": model.wins_by_ko,
        "wins_by_points": model.wins_by_points,
        "image_url": model.image_url,
    }
