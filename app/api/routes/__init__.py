from app.api.routes import health, realtime
from app.api.routes import catalog_inventory, catalog_memberships, catalog_plans, catalog_promotions
from app.api.routes import admin_internal_users, admin_permissions, admin_personal_records, admin_roles
from app.api.routes import gym_ingresos_qr, gym_members, gym_memberships, gym_sales

__all__ = [
    "admin_internal_users",
    "admin_permissions",
    "admin_personal_records",
    "admin_roles",
    "catalog_inventory",
    "catalog_memberships",
    "catalog_plans",
    "catalog_promotions",
    "gym_ingresos_qr",
    "gym_members",
    "gym_memberships",
    "gym_sales",
    "health",
    "realtime",
]
