# icecream_outlet

A production-ready Django REST Framework API for an **ice-cream outlet** with **separate, reusable apps**:
- `accounts` — registration + JWT authentication (via SimpleJWT)
- `flavours` — manage ice-cream flavours
- `toppings` — manage toppings
- `orders` — place orders composed of flavour items + optional toppings

## Features
- Django 5 + DRF
- JWT auth (obtain/refresh/verify)
- Per-app `urls.py`, serializers, viewsets
- Reusable, decoupled apps you can plug into other projects
- OpenAPI schema + Swagger/Redoc via `drf-spectacular`
- Admin configured
- Sensible permissions (read-open, write-authenticated) and pagination

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create env file
cp .env.example .env

# Run migrations and create a superuser
python manage.py migrate
python manage.py createsuperuser

# Start dev server
python manage.py runserver
```

### Environment variables (`.env`)
```
DEBUG=true
SECRET_KEY=change-me
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### API Highlights
- Auth:
  - `POST /api/auth/register/` — create account
  - `POST /api/auth/jwt/create/` — obtain JWT (username & password)
  - `POST /api/auth/jwt/refresh/`
  - `POST /api/auth/jwt/verify/`
  - `GET /api/auth/me/` — current user profile

- Catalogue:
  - `GET/POST /api/flavours/` (list/create)
  - `GET/PUT/PATCH/DELETE /api/flavours/{id}/`
  - `GET/POST /api/toppings/`
  - `GET/PUT/PATCH/DELETE /api/toppings/{id}/`

- Orders:
  - `GET/POST /api/orders/` — create + list user's orders
  - `GET /api/orders/{id}/`

OpenAPI:
- Swagger UI: `/api/schema/swagger/`
- Redoc: `/api/schema/redoc/`

### Tests
Run:
```bash
pytest
```
