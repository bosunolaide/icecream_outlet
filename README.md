# 🍦 Ice Cream Outlet API  
**Django REST Framework + Machine Learning + Docker + CI/CD**

A full-featured backend system for managing an ice cream outlet — built with Django REST Framework, containerized with Docker, enhanced with a machine learning recommender engine, and production-ready with CI/CD via GitHub Actions.

---

## 🚀 Features

✅ Modular architecture with reusable Django apps  
✅ JWT authentication (DRF SimpleJWT)  
✅ Flavours, toppings, and order management  
✅ Machine Learning flavour recommender (KNN + collaborative filtering)  
✅ Auto-generated API docs (Swagger & Redoc)  
✅ PostgreSQL, Gunicorn, and Nginx for production  
✅ MySQL and Celery for analytics/machine learning
✅ Docker + docker-compose for local and production setups  
✅ GitHub Actions CI/CD for automatic testing and deployment  

---

## 🧠 Machine Learning Integration

The app includes a **personalized flavour recommendation engine** powered by `scikit-learn`.  
It analyzes order data and suggests new flavours to users based on similarity patterns.

### Training:
```bash
python manage.py seed_data
python manage.py train_recommender
```

### Usage:
```bash
GET /api/recommendations/flavours/
Authorization: Bearer <token>
```

Response example:
```json
[{"id": 2, "name": "Chocolate", "price": "2.75"}]
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Django 5, Django REST Framework |
| ML | scikit-learn, pandas, joblib |
| Auth | JWT (SimpleJWT) |
| DB | PostgreSQL |
| Web Server | Gunicorn + Nginx |
| Containerization | Docker & docker-compose |
| CI/CD | GitHub Actions |
| Docs | drf-spectacular (Swagger & Redoc) |

---

## 🧱 Local Setup

```bash
git clone https://github.com/<your-username>/icecream_outlet.git
cd icecream_outlet
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Visit:  
👉 [http://127.0.0.1:8000/api/schema/swagger/](http://127.0.0.1:8000/api/schema/swagger/)

---

## 🐳 Docker Setup

### Development
```bash
docker compose up --build
```

### Production
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

---

## ⚡ CI/CD with GitHub Actions

- Runs tests automatically on each push to `main`
- Builds and pushes Docker images to GHCR
- Optionally triggers deployment to Render / Railway / VPS

To deploy automatically to Render:
1. Create a new Web Service in Render connected to your repo
2. Copy the **Deploy Hook URL**
3. Add it as a GitHub secret: `RENDER_DEPLOY_HOOK`

---

## 🌍 API Documentation

| Type | URL |
|------|-----|
| Swagger UI | `/api/schema/swagger/` |
| Redoc | `/api/schema/redoc/` |

---

## 📊 Example ERD

```
User ───< Order ───< OrderItem >─── Flavour
                            │
                            └───< Topping
```

---

## Dual-Database Analytics Extension (PostgreSQL + MySQL) with Celery

**Databases**
- `default` = PostgreSQL (app read/write)
- `analytics` = MySQL (analytics & ML)

**How it works**
- Multi-DB configured in `settings.py`
- `AnalyticsRouter` routes the `analytics` app to MySQL
- `analytics.tasks.sync_to_analytics` copies data hourly via Celery Beat
- `analytics.tasks.train_sales_forecast` shows an example ML task reading from MySQL

**Run with Docker**

```bash
# Base stack (Postgres + web + nginx)
docker compose -f docker-compose.prod.yml up -d

# Add analytics stack (MySQL + Redis + Celery worker/beat)
docker compose -f docker-compose.prod.yml -f docker-compose.override.yml up -d
```

**Migrations**
```bash
docker compose exec web python manage.py migrate --database=default
docker compose exec web python manage.py migrate --database=analytics
```

**Trigger a sync manually (optional)**
```bash
docker compose exec web python manage.py shell -c "from analytics.tasks import sync_to_analytics; sync_to_analytics.delay()"
```
---

## 🧠 Future Enhancements

- ✅ Real-time notifications (Django Channels)
- ✅ Payment integration (Stripe)
- ✅ Recommendation improvements with TensorFlow embeddings
- ✅ Analytics dashboard (React + Chart.js)
- ✅ Caching (Redis)

---

## 💼 Author

👨‍💻 **Abiola Olatunbosun**    
🌐 [linkedin.com/in/abiola-olatunbosun/](https://linkedin.com/in/abiola-olatunbosun/)

> “Built with 🍦 and machine learning.”

---

## 🏁 License

MIT License © 2025
