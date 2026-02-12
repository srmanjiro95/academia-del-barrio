# Academia del Barrio - Backend (FastAPI)

## ¿Ya está lista para integrar?
Sí, ya tienes la base para integrar con tu frontend/proyecto principal:
- API modular por dominios (`catalog`, `admin`, `gym`).
- Realtime con Redis + WebSockets.
- Persistencia SQL en PostgreSQL.
- **Migraciones con Alembic** para crear/versionar tablas de forma correcta.

## Stack de datos
- **PostgreSQL**: persistencia principal de catálogo, admin y gym.
- **Redis**: cache y bus de eventos en tiempo real (pub/sub + WebSockets).

## Requisitos
- Python 3.11+
- PostgreSQL 14+
- Redis

## Configuración

Crear un archivo `.env` (opcional):

```bash
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/academia_del_barrio
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Migraciones (Alembic)

1) Crear la base en PostgreSQL (pgAdmin4 o SQL):
```sql
CREATE DATABASE academia_del_barrio;
```

2) Ejecutar migraciones:
```bash
alembic upgrade head
```

3) (Opcional) Ver historial:
```bash
alembic history
```

4) (Opcional) Crear nuevas migraciones:
```bash
alembic revision --autogenerate -m "tu cambio"
```

## Ejecutar API

```bash
uvicorn app.main:app --reload
```

## Endpoints

### Health
- `GET /health`

### Catálogo
- `GET/POST /catalog/promotions`
- `GET/POST /catalog/inventory`
- `GET/POST /catalog/memberships`
- `GET/POST /catalog/plans`

### Administración
- `GET/POST /admin/roles`
- `GET/POST /admin/permissions`
- `GET/POST /admin/internal-users`
- `GET/POST /admin/personal-records`

### Gym
- `GET/POST /gym/members`
- `GET/POST /gym/memberships`
- `GET/POST /gym/ingresos-qr`
- `GET/POST /gym/sales`

### Tiempo real
- `POST /events` publica eventos en Redis para fan-out a WebSockets.
- `POST /catalog/inventory/{item_id}/discount` publica descuentos de inventario.
- `WS /ws` canal WebSocket para actualizaciones en tiempo real.
