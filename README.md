# Academia del Barrio - Backend (FastAPI)

## Requisitos
- Python 3.11+
- Redis

## Configuración

Crear un archivo `.env` (opcional):

```bash
REDIS_URL=redis://localhost:6379/0
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar

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
