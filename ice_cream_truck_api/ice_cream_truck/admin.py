from django.contrib import admin
from .models import FoodItem, Flavor, IceCreamTruck, Customer

admin.site.register(FoodItem)
admin.site.register(Flavor)
admin.site.register(IceCreamTruck)
admin.site.register(Customer)
