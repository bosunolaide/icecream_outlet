import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from flavours.models import Flavour
from toppings.models import Topping

@pytest.mark.django_db
def test_create_order_flow():
    user = User.objects.create_user(username="bob", password="password123")
    f = Flavour.objects.create(name="Vanilla", price="2.50")
    t = Topping.objects.create(name="Sprinkles", price="0.50")

    client = APIClient()
    tok = client.post("/api/auth/jwt/create/", {"username":"bob","password":"password123"}, format="json").data
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok['access']}")

    payload = {
        "notes": "no nuts",
        "items": [
            {"flavour": f.id, "quantity": 2, "toppings": [t.id]}
        ]
    }
    r = client.post("/api/orders/", payload, format="json")
    assert r.status_code == 201
    order_id = r.data["id"] if "id" in r.data else None
    assert order_id is not None
