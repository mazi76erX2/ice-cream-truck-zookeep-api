from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...models import IceCreamTruck, FoodItem, Flavor

User = get_user_model()


class Command(BaseCommand):
    help: str = "Add default data to the app"

    def handle(self, *args, **kwargs) -> None:
        # Check if data is already added
        if self.data_already_added():
            self.stdout.write(self.style.WARNING("Data already added."))
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
            ice_cream_truck = IceCreamTruck.objects.create(name="Krispy Kream")

            # Create food items if they don't exist
            self.create_food_items(ice_cream_truck)

            self.stdout.write(self.style.SUCCESS("Default data added successfully."))

    def data_already_added(self) -> bool:
        # Check if IceCreamTruck, FoodItem, and Flavor objects exist
        return (
            User.objects.filter(username="zolazookeep").exists()
            and IceCreamTruck.objects.filter(name="Krispy Kream").exists()
            and FoodItem.objects.filter(name="Ice Cream").exists()
        )

    def create_food_items(self, ice_cream_truck: IceCreamTruck) -> None:
        # Create food items
        food_items = [
            FoodItem(name="Ice Cream", price=3.99, ice_cream_truck=ice_cream_truck),
            FoodItem(name="Shaved Ice", price=2.99, ice_cream_truck=ice_cream_truck),
            FoodItem(name="Snack Bar", price=1.99, ice_cream_truck=ice_cream_truck),
        ]
        FoodItem.objects.bulk_create(food_items)

        # Create flavorss
        self.create_flavors()

    def create_flavors(self) -> None:
        # Create flavors for Ice Cream
        ice_cream = FoodItem.objects.get(name="Ice Cream")
        flavors = [
            Flavor(name="Chocolate", food_item=ice_cream),
            Flavor(name="Pistachio", food_item=ice_cream),
            Flavor(name="Strawberry", food_item=ice_cream),
            Flavor(name="Mint", food_item=ice_cream),
        ]

        # Create flavors for Shaved Ice
        shaved_ice = FoodItem.objects.get(name="Shaved Ice")
        flavors += [
            Flavor(name="Blueberry", food_item=shaved_ice),
            Flavor(name="Orange", food_item=shaved_ice),
            Flavor(name="Strawberry", food_item=shaved_ice),
        ]

        # Create flavors for Snack Bar
        snack_bar = FoodItem.objects.get(name="Snack Bar")
        flavors += [
            Flavor(name="Klondike", food_item=snack_bar),
            Flavor(name="Magnum", food_item=snack_bar),
            Flavor(name="Twister", food_item=snack_bar),
        ]

        Flavor.objects.bulk_create(flavors)
