from fastapi import APIRouter

from app.schemas.catalog import DevelopmentPlan, DevelopmentPlanBase

router = APIRouter(prefix="/catalog/plans", tags=["catalog-plans"])


@router.get("", response_model=list[DevelopmentPlan])
async def list_plans() -> list[DevelopmentPlan]:
    return []


@router.post("", response_model=DevelopmentPlan)
async def create_plan(payload: DevelopmentPlanBase) -> DevelopmentPlan:
    return DevelopmentPlan(id="plan_1", **payload.model_dump())


@router.get("/{plan_id}", response_model=DevelopmentPlan)
async def get_plan(plan_id: str) -> DevelopmentPlan:
    return DevelopmentPlan(
        id=plan_id,
        name="",
        description="",
        member_id="",
        member_name="",
        focus="",
        coach="",
        sessions_per_week=0,
    )
