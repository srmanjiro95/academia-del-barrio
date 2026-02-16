import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.services.realtime import start_listener

OPENAPI_TAGS = [
    {"name": "health", "description": "Estado general del servicio."},
    {"name": "realtime", "description": "Publicación de eventos para tiempo real."},
    {"name": "catalog-inventory", "description": "Inventario de productos."},
    {"name": "catalog-promotions", "description": "Promociones activas e históricas."},
    {"name": "catalog-memberships", "description": "Catálogo de membresías."},
    {"name": "catalog-plans", "description": "Planes de desarrollo."},
    {"name": "admin-roles", "description": "Gestión de roles."},
    {"name": "admin-permissions", "description": "Gestión de permisos."},
    {"name": "admin-internal-users", "description": "Gestión de usuarios internos."},
    {"name": "admin-personal-records", "description": "Historial deportivo/personal."},
    {"name": "gym-members", "description": "Gestión de miembros del gym."},
    {"name": "gym-memberships", "description": "Asignaciones de membresía por miembro."},
    {"name": "gym-ingresos-qr", "description": "Check-ins vía QR."},
    {"name": "gym-sales", "description": "Ventas y movimientos comerciales."},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    stop_event = asyncio.Event()
    listener_task = asyncio.create_task(start_listener(stop_event))
    yield
    stop_event.set()
    await listener_task


app = FastAPI(
    title=settings.app_name,
    description=(
        "Backend de Academia del Barrio con módulos de catálogo, administración y gym. "
        "Incluye eventos en tiempo real sobre Redis y WebSockets."
    ),
    version="1.0.0",
    openapi_tags=OPENAPI_TAGS,
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# 🔥 CORS para Vite + React
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
