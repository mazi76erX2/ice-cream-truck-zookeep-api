import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_food_items(client):
    url = reverse("fooditem-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_ice_cream_truck_inventory(client):
    url = reverse("ice_cream_truck_inventory")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_ice_cream_truck_revenue(client):
    url = reverse("ice_cream_truck_revenue")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_buy_food(client):
    url = reverse("buy_food")
    data = {"food_item_id": 1, "customer_id": 1, "quantity": 2}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
