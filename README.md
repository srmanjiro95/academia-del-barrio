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
- Al crear miembro se autocompletan `membership_start_date`, `membership_end_date`, `membership_price` y se crea vínculo en `member_memberships` cuando se envía `membership_id`.
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
- `PUT /catalog/promotions/{promotion_id}`
- `GET/POST /catalog/inventory`
- `PUT /catalog/inventory/{item_id}`
- `GET/POST /catalog/memberships`
- `PUT /catalog/memberships/{membership_id}`
- `GET/POST /catalog/plans`
- `PUT /catalog/plans/{plan_id}`
  - En planes, `member_id` es opcional (catálogo sin asignación inmediata).
- `PUT /catalog/plans/{plan_id}` para editar plan y asignación opcional de miembro.

### Administración
- `GET/POST /admin/roles`
- `PUT /admin/roles/{role_id}`
- `GET/POST /admin/permissions`
- `PUT /admin/permissions/{permission_id}`
- `GET/POST /admin/internal-users`
- `PUT /admin/internal-users/{user_id}`
- `GET/POST /admin/personal-records`
- `PUT /admin/personal-records/{record_id}`

### Gym
- `GET/POST /gym/members`
- `PUT /gym/members/{member_id}`
- `POST /gym/members/{member_id}/refresh-qr` regenera UUID y reenvía correo con nuevo QR.
- `GET/POST /gym/memberships`
- `PUT /gym/memberships/{membership_id}`
- `GET/POST /gym/ingresos-qr` (POST recibe `{ "qr_uuid": "..." }`, registra ingreso y devuelve card para modal con info de miembro + récord de peleas).
- `PUT /gym/ingresos-qr/{entry_id}`
- `GET/POST /gym/sales`
- `PUT /gym/sales/{sale_id}`

### Promociones (nueva lógica de alcance)
- `applies_to` define alcance: `all_store`, `category`, `products`, `membership`.
- `target_category` se usa cuando `applies_to=category`.
- `target_product_ids` se usa cuando `applies_to=products`.
- `target_membership_ids` se usa cuando `applies_to=membership`.
- Para `type=Inscripción`, la promoción debe aplicarse a **un solo producto** (`applies_to=products` con un elemento).

### Inventario
- Se añadió `category` (string) para clasificar productos en catálogos específicos.

### Tiempo real
- `POST /events` publica eventos en Redis para fan-out a WebSockets.
- `WS /ws` envía snapshots iniciales y eventos en tópicos: `inventory.updated`, `promotions.updated`, `members.updated`.
- Puedes suscribirte por tópicos enviando: `{ "action": "subscribe", "topics": ["inventory.updated"] }`.
- `POST /catalog/inventory/{item_id}/discount` también emite `inventory.updated`.
