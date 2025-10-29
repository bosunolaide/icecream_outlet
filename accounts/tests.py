import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_and_me():
    client = APIClient()
    resp = client.post(reverse("register"), {"username":"alice","password":"password123"} , format="json")
    assert resp.status_code == 201
    # login
    tok = client.post(reverse("jwt-create"), {"username":"alice","password":"password123"}, format="json").data
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok['access']}")
    me = client.get(reverse("me"))
    assert me.status_code == 200
    assert me.data["username"] == "alice"
