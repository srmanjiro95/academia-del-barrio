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
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_USE_TLS=false
SMTP_FROM_EMAIL=no-reply@academiadelbarrio.local
PUBLIC_BASE_URL=http://localhost:8000
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

## Documentación Swagger / OpenAPI

- Swagger UI: `http://localhost:8000/swagger`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

Con esto puedes probar endpoints de forma rápida desde Swagger (sin Postman) y validar request/response models.

## Persistencia real y archivos

- Correo de registro automático al crear miembro (`/gym/members`) con membresía, vigencia, precio y QR único.
- Endpoint independiente para regenerar UUID/QR y reenviar correo: `POST /gym/members/{member_id}/refresh-qr`.

- Los endpoints de **Inventario**, **Membresías**, **Usuarios internos** y **Record personal** ya guardan en PostgreSQL.
- Las imágenes se guardan localmente en `media/uploads/` dentro del proyecto BE.
- Se exponen públicamente en `http://localhost:8000/media/...`.

### Endpoints de carga de imagen
> Nota: estos endpoints reciben `multipart/form-data` con campo `file`.
- `POST /uploads/image?folder=memberships` endpoint global de upload; devuelve URL absoluta + ruta relativa.
- `POST /catalog/inventory/{item_id}/image`
- `POST /catalog/memberships/upload-image` (compatibilidad) carga archivo y devuelve `image_url` absoluta.
- `POST /catalog/memberships/{membership_id}/image` asigna imagen a una membresía existente.
- `POST /admin/internal-users/{user_id}/image`
- `POST /admin/personal-records/{record_id}/image`

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
- `POST /gym/members/{member_id}/refresh-qr` regenera UUID y reenvía correo con nuevo QR.
- `GET/POST /gym/memberships`
- `GET/POST /gym/ingresos-qr`
- `GET/POST /gym/sales`

### Tiempo real
- `POST /events` publica eventos en Redis para fan-out a WebSockets.
- `WS /ws` envía snapshots iniciales y eventos en tópicos: `inventory.updated`, `promotions.updated`, `members.updated`.
- Puedes suscribirte por tópicos enviando: `{ "action": "subscribe", "topics": ["inventory.updated"] }`.
- `POST /catalog/inventory/{item_id}/discount` también emite `inventory.updated`.
