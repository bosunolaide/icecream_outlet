FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/ml_models
RUN python manage.py collectstatic --noinput || true

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app /app

RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "icecream_outlet.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
