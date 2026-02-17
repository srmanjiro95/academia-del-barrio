from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import DevelopmentPlanModel
from app.schemas.catalog import DevelopmentPlan, DevelopmentPlanBase

router = APIRouter(prefix="/catalog/plans", tags=["catalog-plans"])


@router.get("", response_model=list[DevelopmentPlan])
async def list_plans(db: AsyncSession = Depends(get_db)) -> list[DevelopmentPlan]:
    rows = (await db.execute(select(DevelopmentPlanModel))).scalars().all()
    return [DevelopmentPlan(**_to_dict(row)) for row in rows]


@router.post("", response_model=DevelopmentPlan)
async def create_plan(payload: DevelopmentPlanBase, db: AsyncSession = Depends(get_db)) -> DevelopmentPlan:
    model = DevelopmentPlanModel(id=uuid4().hex, **payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return DevelopmentPlan(**_to_dict(model))


@router.get("/{plan_id}", response_model=DevelopmentPlan)
async def get_plan(plan_id: str, db: AsyncSession = Depends(get_db)) -> DevelopmentPlan:
    model = await db.get(DevelopmentPlanModel, plan_id)
    if not model:
        raise HTTPException(status_code=404, detail="Development plan not found")
    return DevelopmentPlan(**_to_dict(model))


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
