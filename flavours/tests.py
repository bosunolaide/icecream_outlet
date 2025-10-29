import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_flavours_list_open():
    client = APIClient()
    resp = client.get("/api/flavours/")
    assert resp.status_code == 200
