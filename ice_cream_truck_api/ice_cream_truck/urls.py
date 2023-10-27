from django.urls import include, path
from .views import (
    FoodItemViewSet,
    IceCreamTruckInventoryView,
    IceCreamTruckRevenueView,
    BuyFoodView,
    AddDefaultDataView,
)
from rest_framework.routers import DefaultRouter

router: DefaultRouter = DefaultRouter()
router.register(r"food_items", FoodItemViewSet)

urlpatterns: list = [
    path("", include(router.urls)),
    path("add_default_data/", AddDefaultDataView.as_view(), name="add_default_data"),
    path(
        "inventory/<int:pk>/",
        IceCreamTruckInventoryView.as_view(),
        name="ice_cream_truck_inventory",
    ),
    path(
        "revenue/", IceCreamTruckRevenueView.as_view(), name="ice_cream_truck_revenue"
    ),
    path("buy_food/", BuyFoodView.as_view(), name="buy_food"),
]
