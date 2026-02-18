from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import DevelopmentPlanModel, GymMemberModel
from app.schemas.catalog import DevelopmentPlan, DevelopmentPlanBase

router = APIRouter(prefix="/catalog/plans", tags=["catalog-plans"])


@router.get("", response_model=list[DevelopmentPlan])
async def list_plans(db: AsyncSession = Depends(get_db)) -> list[DevelopmentPlan]:
    rows = (await db.execute(select(DevelopmentPlanModel))).scalars().all()
    return [DevelopmentPlan(**_to_dict(row)) for row in rows]


@router.post("", response_model=DevelopmentPlan)
async def create_plan(payload: DevelopmentPlanBase, db: AsyncSession = Depends(get_db)) -> DevelopmentPlan:
    member_id, member_name = await _resolve_member_assignment(db, payload.member_id, payload.member_name)

    model = DevelopmentPlanModel(
        id=uuid4().hex,
        name=payload.name,
        description=payload.description,
        member_id=member_id,
        member_name=member_name,
        focus=payload.focus,
        coach=payload.coach,
        sessions_per_week=payload.sessions_per_week,
    )
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return DevelopmentPlan(**_to_dict(model))


@router.put("/{plan_id}", response_model=DevelopmentPlan)
async def update_plan(plan_id: str, payload: DevelopmentPlanBase, db: AsyncSession = Depends(get_db)) -> DevelopmentPlan:
    model = await db.get(DevelopmentPlanModel, plan_id)
    if not model:
        raise HTTPException(status_code=404, detail="Development plan not found")

    member_id, member_name = await _resolve_member_assignment(db, payload.member_id, payload.member_name)

    model.name = payload.name
    model.description = payload.description
    model.member_id = member_id
    model.member_name = member_name
    model.focus = payload.focus
    model.coach = payload.coach
    model.sessions_per_week = payload.sessions_per_week

    await db.commit()
    await db.refresh(model)
    return DevelopmentPlan(**_to_dict(model))


@router.get("/{plan_id}", response_model=DevelopmentPlan)
async def get_plan(plan_id: str, db: AsyncSession = Depends(get_db)) -> DevelopmentPlan:
    model = await db.get(DevelopmentPlanModel, plan_id)
    if not model:
        raise HTTPException(status_code=404, detail="Development plan not found")
    return DevelopmentPlan(**_to_dict(model))


async def _resolve_member_assignment(
    db: AsyncSession,
    raw_member_id: str | None,
    raw_member_name: str | None,
) -> tuple[str | None, str | None]:
    member_id = (raw_member_id or "").strip() or None
    member_name = (raw_member_name or "").strip() or None

    if member_id is None:
        return None, member_name

    member = await db.get(GymMemberModel, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Assigned member not found")

    resolved_name = member_name or f"{member.first_name} {member.last_name} {member.middle_name}".strip()
    return member_id, resolved_name


def _to_dict(model: DevelopmentPlanModel) -> dict:
    return {
        "id": model.id,
        "name": model.name,
        "description": model.description,
        "member_id": model.member_id,
        "member_name": model.member_name,
        "focus": model.focus,
        "coach": model.coach,
        "sessions_per_week": model.sessions_per_week,
    }
