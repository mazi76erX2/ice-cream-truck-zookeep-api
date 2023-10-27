Ice Cream Truck API
-------------------

This API allows users to buy food items, such as ice creams, shaved ice, and snack bars, from an ice cream truck. The API also provides information about the inventory of the ice cream truck and the total amount of money the ice cream truck has made.

# Installation

1. Clone the repository.
https://github.com/mazi76erX2/ice-cream-truck-zookeep-api.git

To run the Django app, you will need to have the following installed:

-   Python 3.11.4 or higher
-   Pipenv
-   Docker

Once you have installed all of the required dependencies, you can clone the repository and install the requirements:

```
git clone https://github.com/mazi76erX2/ice-cream-truck-zookeep-api.git
make install_requirements
cd ice-cream-truck-api

```

2. Copy the .env.example file to .env and update the values as needed.



## Running the Django app using Docker-Compose

To run the Django app using Docker-compose, simply run the following command:

```
make up

```

This will build the Docker image for the Django app and then start the Django app in a Docker container. You can then access the app at `http://localhost:8000`.

to stoop the app run

```
make down

```

> Please note: You will need to create your own database in postgres using the config found in .env.example  wheen runniing locally.

## Running the Django app locally


To run the Django app locally, simply run the following command:

```
make local

```

This will start the Django app on port 8000. You can then access the app at `http://localhost:8000`.

## Running the Django app using Docker

To run the Django app using Docker, simply run the following command:

```
make dev_up

```

This will build the Docker image for the Django app and then start the Django app in a Docker container. You can then access the app at `http://localhost:8000`.

## Running Django management commands using Docker

To run a Django management command using Docker, simply run the following command:

```
make dev_web_exec CMD=<Django management command>

```

For example, to run the Django management command `migrate`, you would run the following command:

```
make dev_web_exec CMD=migrate

```

## Linting the code

To lint the code, simply run the following command:

```
make lint

```

This will run Pylint and Mypy on the code to check for errors.

## Testing the code

To test the code, simply run the following command:

```
make test

```

This will run all of the tests for the Django app.

## Deploying the Django app

To deploy the Django app to production, you can use the following steps:

1.  Build the Docker image for the Django app:

```
make dev_build

```

1.  Push the Docker image to a registry:

```
docker push your-registry.com/ice-cream-truck-api

```

1.  Deploy the Docker image to production using a tool such as Kubernetes or Docker Compose.

## Additional commands

The following are some additional commands that you can use:

-   `make format`: Formats the code with Black.
-   `make install_requirements`: Installs the requirements locally.
-   `make dev_down`: Stops and removes the Docker container.


# Endpoints:

-   `/add_default_data/`: This endpoint adds default data to the database, including a superuser, an ice cream truck, and some food items.
-   `/inventory/<int:pk>/`: This endpoint retrieves the inventory of the ice cream truck with the given ID.
-   `/revenue/`: This endpoint retrieves the total amount of money the ice cream truck has made.
-   `/buy_food/`: This endpoint allows users to buy food items from the ice cream truck.

# Example requests:

```
# Add default data
POST /add_default_data/

# Retrieve the inventory of the ice cream truck with ID 1
GET /inventory/1/

# Retrieve the total amount of money the ice cream truck has made
GET /revenue/

# Buy 2 ice creams from the ice cream truck with ID 1
POST /buy_food/
{
    "food_item_id": 1,
    "customer_id": 1,
    "ice_cream_truck_id": 1,
    "quantity": 2
}

```

Example responses:

```
# Add default data response
HTTP/1.1 200 OK
Content-Type: application/json

{
    "message": "Default data added successfully."
}

# Retrieve the inventory of the ice cream truck with ID 1 response
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "name": "Krispy Kream",
    "food_items": [
        {
            "id": 1,
            "name": "Ice Cream",
            "price": 3.99,
            "stock": 10
        },
        {
            "id": 2,
            "name": "Shaved Ice",
            "price": 2.99,
            "stock": 5
        },
        {
            "id": 3,
            "name": "Snack Bar",
            "price": 1.99,
            "stock": 15
        }
    ]
}

# Retrieve the total amount of money the ice cream truck has made response
HTTP/1.1 200 OK
Content-Type: application/json

{
    "total_revenue": 10.97
}

# Buy 2 ice creams from the ice cream truck with ID 1 response
HTTP/1.1 200 OK
Content-Type: application/json

{
    "message": "ENJOY!"
}

```

Conclusion:

This API provides a simple way for users to buy food items from an ice cream truck and for ice cream truck owners to track their inventory and revenue.
