from rest_framework import serializers
from .models import FoodItem, Flavor, IceCreamTruck


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model: type[Flavor] = Flavor
        fields: tuple[str, ...] = ("name",)


class FoodItemSerializer(serializers.ModelSerializer):
    flavors: FlavorSerializer = FlavorSerializer(many=True, read_only=True)

    class Meta:
        model: type[FoodItem] = FoodItem
        fields: tuple[str, ...] = ("name", "price", "flavors")


class IceCreamTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = IceCreamTruck
        fields = "__all__"
