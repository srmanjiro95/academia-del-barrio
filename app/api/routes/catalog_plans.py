from fastapi import APIRouter

from app.schemas.catalog import Plan, PlanBase

router = APIRouter(prefix="/catalog/plans", tags=["catalog-plans"])


@router.get("", response_model=list[Plan])
async def list_plans() -> list[Plan]:
    return []


@router.post("", response_model=Plan)
async def create_plan(payload: PlanBase) -> Plan:
    return Plan(id="plan_1", **payload.model_dump())


@router.get("/{plan_id}", response_model=Plan)
async def get_plan(plan_id: str) -> Plan:
    return Plan(id=plan_id, name="", description=None, price=0.0)
