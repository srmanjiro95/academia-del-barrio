from fastapi import APIRouter

from app.api.routes import (
    admin_internal_users,
    admin_permissions,
    admin_personal_records,
    admin_roles,
    catalog_inventory,
    catalog_memberships,
    catalog_plans,
    catalog_promotions,
    gym_ingresos_qr,
    gym_members,
    gym_memberships,
    gym_sales,
    health,
    realtime,
    uploads,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(realtime.router)
api_router.include_router(uploads.router)

api_router.include_router(catalog_promotions.router)
api_router.include_router(catalog_inventory.router)
api_router.include_router(catalog_memberships.router)
api_router.include_router(catalog_plans.router)

api_router.include_router(admin_roles.router)
api_router.include_router(admin_permissions.router)
api_router.include_router(admin_internal_users.router)
api_router.include_router(admin_personal_records.router)

api_router.include_router(gym_memberships.router)
api_router.include_router(gym_members.router)
api_router.include_router(gym_ingresos_qr.router)
api_router.include_router(gym_sales.router)
