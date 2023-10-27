from typing import Any

from django.db.models.query import QuerySet
from django.db.models import Sum, F
from django.contrib.auth import get_user_model

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FoodItem, IceCreamTruck, Customer, Transaction, Flavor
from .serializers import FoodItemSerializer, IceCreamTruckSerializer

User = get_user_model()


class AddDefaultDataView(APIView):
    def post(self, request) -> Response:
        response_data: dict[str, Any]
        status_code: int

        if self.data_already_added():
            response_data = {"message": "Data already added."}
            status_code = 400
        else:
            # Create superuser
            User.objects.create(
                username="zolazookeep",
                email="zola@zookeep.com",
                password="root",
                first_name="Zola",
                last_name="Zookeep",
                is_staff=True,
                is_superuser=True,
            )
            # Create Ice Cream Truck
            ice_cream_truck: IceCreamTruck = IceCreamTruck.objects.create(
                name="Krispy Kream"
            )

            # Create food items if they don't exist
            self.create_food_items(ice_cream_truck)

            response_data = {"message": "Default data added successfully."}
            status_code = 200

        return Response(response_data, status=status_code)

    def data_already_added(self) -> bool:
        # Check if IceCreamTruck, FoodItem, and Flavor objects exist
        return (
            User.objects.filter(username="zolazookeep").exists()
            and IceCreamTruck.objects.filter(name="Krispy Kream").exists()
            and FoodItem.objects.filter(name="Ice Cream").exists()
        )

    def create_food_items(self, ice_cream_truck: IceCreamTruck) -> None:
        # Create food items
        food_items: list[FoodItem] = [
            FoodItem(name="Ice Cream", price=3.99, ice_cream_truck=ice_cream_truck),
            FoodItem(name="Shaved Ice", price=2.99, ice_cream_truck=ice_cream_truck),
            FoodItem(name="Snack Bar", price=1.99, ice_cream_truck=ice_cream_truck),
        ]
        FoodItem.objects.bulk_create(food_items)

        # Create flavorss
        self.create_flavors()

    def create_flavors(self) -> None:
        # Create flavors for Ice Cream
        ice_cream: FoodItem = FoodItem.objects.get(name="Ice Cream")
        flavors: list[Flavor] = [
            Flavor(name="Chocolate", food_item=ice_cream),
            Flavor(name="Pistachio", food_item=ice_cream),
            Flavor(name="Strawberry", food_item=ice_cream),
            Flavor(name="Mint", food_item=ice_cream),
        ]

        # Create flavors for Shaved Ice
        shaved_ice: FoodItem = FoodItem.objects.get(name="Shaved Ice")
        flavors += [
            Flavor(name="Blueberry", food_item=shaved_ice),
            Flavor(name="Orange", food_item=shaved_ice),
            Flavor(name="Strawberry", food_item=shaved_ice),
        ]

        # Create flavors for Snack Bar
        snack_bar: FoodItem = FoodItem.objects.get(name="Snack Bar")
        flavors += [
            Flavor(name="Klondike", food_item=snack_bar),
            Flavor(name="Magnum", food_item=snack_bar),
            Flavor(name="Twister", food_item=snack_bar),
        ]

        Flavor.objects.bulk_create(flavors)


class FoodItemDetailView(generics.RetrieveAPIView):
    queryset: QuerySet[FoodItem] = FoodItem.objects.all()
    serializer_class: type[FoodItemSerializer] = FoodItemSerializer


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[FoodItem] = FoodItem.objects.all()
    serializer_class: type[FoodItemSerializer] = FoodItemSerializer


class IceCreamTruckInventoryView(generics.RetrieveAPIView):
    queryset = IceCreamTruck.objects.all()
    serializer_class = IceCreamTruckSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class IceCreamTruckRevenueView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        ice_cream_truck = IceCreamTruck.objects.first()
        total_revenue = Transaction.objects.filter(
            ice_cream_truck=ice_cream_truck
        ).aggregate(total_revenue=Sum(F("total")))["total_revenue"]
        total_revenue = total_revenue or 0
        return Response({"total_revenue": total_revenue})


class BuyFoodView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        food_item_id = request.data.get("food_item_id")
        customer_id = request.data.get("customer_id")
        ice_cream_truck_id = request.data.get("ice_cream_truck_id")
        quantity = request.data.get("quantity")

        try:
            food_item = FoodItem.objects.get(id=food_item_id)
            customer = Customer.objects.get(id=customer_id)
            ice_cream_truck = IceCreamTruck.objects.get(id=ice_cream_truck_id)

            if quantity > food_item.stock:
                return Response(
                    {"message": "SORRY!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total_price = food_item.price * quantity
            if customer.balance < total_price:
                return Response(
                    {"message": "SORRY!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update stock and customer balance
            food_item.stock -= quantity
            food_item.save()
            customer.balance -= total_price
            customer.save()

            # Create transaction
            Transaction.objects.create(
                food_item=food_item,
                customer=customer,
                ice_cream_truck=ice_cream_truck,
                quantity=quantity,
                total=total_price,
            )

            return Response({"message": "ENJOY!"}, status=status.HTTP_200_OK)

        except FoodItem.DoesNotExist:
            return Response(
                {"message": "Invalid food item ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Customer.DoesNotExist:
            return Response(
                {"message": "Invalid customer ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        except IceCreamTruck.DoesNotExist:
            return Response(
                {"message": "Invalid ice cream truck ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
