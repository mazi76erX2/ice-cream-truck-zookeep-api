from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class FoodItem(models.Model):
    name: models.CharField = models.CharField(
        max_length=100,
        unique=True,
    )
    price: models.DecimalField = models.DecimalField(max_digits=6, decimal_places=2)
    stock: models.IntegerField = models.SmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Flavor(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    food_item: models.ForeignKey = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class IceCreamTruck(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    food_items: models.ManyToManyField = models.ManyToManyField(FoodItem)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    balance: models.DecimalField = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=6
    )

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} - ${self.balance}"


class Transaction(models.Model):
    food_item: models.ForeignKey = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    customer: models.ForeignKey = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ice_cream_truck: models.ForeignKey = models.ForeignKey(
        IceCreamTruck, on_delete=models.CASCADE
    )
    quantity: models.IntegerField = models.IntegerField()
    total: models.DecimalField = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=6
    )
    date: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.customer} bought {self.quantity} {self.food_item.name} for {self.total} on {self.date}"
