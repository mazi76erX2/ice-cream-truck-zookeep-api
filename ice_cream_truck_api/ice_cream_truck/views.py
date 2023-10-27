from typing import Any

from django.db.models.query import QuerySet
from django.db.models import Sum, F
from django.core.management import call_command

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FoodItem, IceCreamTruck, Customer, Transaction
from .serializers import FoodItemSerializer, IceCreamTruckSerializer


class AddDefaultDataView(APIView):
    def post(self, request) -> Response:
        try:
            # Call the management command
            call_command("add_default_data")
            response_data: dict[str, Any] = {
                "message": "Default data added successfully."
            }
            status_code: int = 200
        except Exception as e:
            response_data = {"message": "Data already added."}
            status_code = 400

        return Response(response_data, status=status_code)


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
