from fastapi import APIRouter

from app.schemas.admin import PersonalRecord, PersonalRecordBase

router = APIRouter(prefix="/admin/personal-records", tags=["admin-personal-records"])


@router.get("", response_model=list[PersonalRecord])
async def list_personal_records() -> list[PersonalRecord]:
    return []


@router.post("", response_model=PersonalRecord)
async def create_personal_record(payload: PersonalRecordBase) -> PersonalRecord:
    return PersonalRecord(id="record_1", **payload.model_dump())


@router.get("/{record_id}", response_model=PersonalRecord)
async def get_personal_record(record_id: str) -> PersonalRecord:
    return PersonalRecord(
        id=record_id,
        member_id="",
        member_name="",
        category="Sparring",
        wins=0,
        losses=0,
        draws=0,
        wins_by_ko=0,
        wins_by_points=0,
    )
