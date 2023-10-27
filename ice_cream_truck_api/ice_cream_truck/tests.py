from typing import Optional

from unittest.mock import patch

import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import FoodItem, IceCreamTruck, Customer, Transaction, Flavor

User = get_user_model()


# Fixtures
@pytest.fixture
def api_client() -> APIClient:
    # Create a test API client
    return APIClient()


@pytest.fixture
def superuser():
    # Create a superuser for authentication
    return User.objects.create(
        username="admin",
        email="admin@example.com",
        password="admin",
        is_superuser=True,
        is_staff=True,
    )


# Unit tests
@pytest.mark.django_db
def test_add_default_data_view(api_client: APIClient, superuser) -> None:
    # Ensure the add_default_data view works correctly
    api_client.force_authenticate(user=superuser)
    url = reverse("add-default-data")
    response = api_client.post(url)
    assert response.status_code == 200
    assert response.data["message"] == "Default data added successfully."


@pytest.mark.django_db
def test_add_default_data_view_already_added(api_client: APIClient, superuser) -> None:
    # Ensure the add_default_data view returns an error if data is already added
    api_client.force_authenticate(user=superuser)
    url = reverse("add-default-data")
    # Add default data
    api_client.post(url)
    # Try adding default data again
    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data["message"] == "Data already added."


@pytest.mark.django_db
def test_food_item_detail_view(api_client: APIClient) -> None:
    # Ensure the food_item_detail view works correctly
    food_item = FoodItem.objects.create(name="Ice Cream", price=2.5)
    url = reverse("food-item-detail", args=[food_item.pk])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == "Ice Cream"


@pytest.mark.django_db
def test_food_item_detail_view_not_found(api_client: APIClient) -> None:
    # Ensure the food_item_detail view returns an error if the food item is not found
    url = reverse("food-item-detail", args=[1])
    response = api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_ice_cream_truck_inventory_view(api_client: APIClient) -> None:
    # Ensure the ice_cream_truck_inventory view works correctly
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")
    url = reverse("ice-cream-truck-inventory")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == "Krispy Kream"


@pytest.mark.django_db
def test_ice_cream_truck_inventory_view_not_found(api_client: APIClient) -> None:
    # Ensure the ice_cream_truck_inventory view returns an error if the ice cream truck is not found
    url = reverse("ice-cream-truck-inventory")
    response = api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_ice_cream_truck_revenue_view(api_client: APIClient) -> None:
    # Ensure the ice_cream_truck_revenue view works correctly
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")
    transaction = Transaction.objects.create(
        ice_cream_truck=ice_cream_truck, total=10.0
    )
    url = reverse("ice-cream-truck-revenue")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["total_revenue"] == 10.0


@pytest.mark.django_db
def test_ice_cream_truck_revenue_view_no_transactions(api_client: APIClient) -> None:
    # Ensure the ice_cream_truck_revenue view returns 0 revenue if there are no transactions
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")
    url = reverse("ice-cream-truck-revenue")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["total_revenue"] == 0.0


@pytest.mark.django_db
def test_buy_food_view(api_client: APIClient) -> None:
    # Ensure the buy_food view works correctly
    food_item = FoodItem.objects.create(name="Ice Cream", price=2.5, stock=10)
    customer = Customer.objects.create(name="John Doe", balance=100.0)
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")
    url = reverse("buy-food")
    data = {"food_item_id": food_item.pk, "customer_id": customer.pk}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data["message"] == "Food item purchased successfully."


@pytest.mark.django_db
def test_buy_food_view_insufficient_balance(api_client: APIClient) -> None:
    # Ensure the buy_food view returns an error if the customer has insufficient balance
    food_item = FoodItem.objects.create(name="Ice Cream", price=2.5, stock=10)
    customer = Customer.objects.create(name="John Doe", balance=1.0)
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")
    url = reverse("buy-food")
    data = {"food_item_id": food_item.pk, "customer_id": customer.pk}
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert response.data["message"] == "Insufficient balance."


@pytest.mark.django_db
def test_buy_food_view_out_of_stock(api_client: APIClient) -> None:
    # Ensure the buy_food view returns an error if the food item is out of stock
    food_item = FoodItem.objects.create(name="Ice Cream", price=2.5, stock=0)
    customer = Customer.objects.create(name="John Doe", balance=100.0)
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")
    url = reverse("buy-food")
    data = {"food_item_id": food_item.pk, "customer_id": customer.pk}
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert response.data["message"] == "Food item is out of stock."


@pytest.mark.django_db
def test_buy_food_view_invalid_customer(api_client: APIClient) -> None:
    # Ensure the buy_food view returns an error if the customer is not found
    food_item = FoodItem.objects.create(name="Ice Cream", price=2.5, stock=10)
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")
    url = reverse("buy-food")
    data = {"food_item_id": food_item.pk, "customer_id": 1}
    response = api_client.post(url, data)
    assert response.status_code == 404
    assert response.data["message"] == "Customer not found."


@pytest.mark.django_db
def test_buy_food_view_invalid_food_item(api_client: APIClient) -> None:
    # Ensure the buy_food view returns an error if the food item is not found
    customer = Customer.objects.create(name="John Doe", balance=100.0)
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")
    url = reverse("buy-food")
    data = {"food_item_id": 1, "customer_id": customer.pk}
    response = api_client.post(url, data)
    assert response.status_code == 404
    assert response.data["message"] == "Food item not found."


# Integration tests
@pytest.mark.django_db
def test_buy_food_integration(
    api_client: APIClient,
    food_item: Optional[FoodItem] = None,
    customer: Optional[Customer] = None,
    ice_cream_truck: Optional[IceCreamTruck] = None,
):
    # Create a food item
    if food_item is None:
        food_item = FoodItem.objects.create(name="Ice Cream", price=2.5, stock=10)

    # Create a customer
    if customer is None:
        customer = Customer.objects.create(name="John Doe", balance=100.0)

    # Create an ice cream truck
    if ice_cream_truck is None:
        ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")

    # Buy the food item
    url = reverse("buy-food")
    data = {
        "food_item_id": food_item.pk,
        "customer_id": customer.pk,
        "ice_cream_truck_id": ice_cream_truck.pk,
        "quantity": 3,
    }
    response = api_client.post(url, data)

    # Assert that the purchase was successful
    assert response.status_code == 200
    assert response.data["message"] == "ENJOY!"

    # Assert that the customer's balance has been updated
    customer.refresh_from_db()
    assert customer.balance == 92.5

    # Assert that the food item's stock has been updated
    food_item.refresh_from_db()
    assert food_item.stock == 7


@patch.object(FoodItem, "refresh_from_db")
@patch.object(Customer, "refresh_from_db")
def test_buy_food_integration_with_patch(
    mock_food_item_refresh_from_db, mock_customer_refresh_from_db, api_client: APIClient
):
    # Create a food item
    food_item = FoodItem.objects.create(name="Ice Cream", price=2.5, stock=10)

    # Create a customer
    customer = Customer.objects.create(name="John Doe", balance=100.0)

    # Create an ice cream truck
    ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")

    # Buy the food item
    url = reverse("buy-food")
    data = {
        "food_item_id": food_item.pk,
        "customer_id": customer.pk,
        "ice_cream_truck_id": ice_cream_truck.pk,
        "quantity": 3,
    }
    api_client.post(url, data)

    # Assert that the refresh_from_db methods were called
    mock_food_item_refresh_from_db.assert_called_once()
    mock_customer_refresh_from_db.assert_called_once()
