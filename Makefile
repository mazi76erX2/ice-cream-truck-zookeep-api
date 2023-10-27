# Install requirements locally
install_requirements:
	pipenv install --dev --system

# Run the Django app locally
local:
	python manage.py runserver

up:
    docker-compose up --build

down:
    docker-compose down

# Build the Docker image
dev_build:
	docker build -t ice_cream_truck_api .

# Run the Django app using Docker
dev_up:
	docker run -p 8000:8000 ice_cream_truck_api

# Run a Django management command using Docker
dev_web_exec:
	docker exec -it ice_cream_truck_api python manage.py $(CMD)

# Clean up the Docker container
dev_down:
	docker stop ice_cream_truck_api && docker rm ice_cream_truck_api

# Lint the code
lint:
	pylint && mypy

# Test the code
test:
	pytest ice_cream_truck_api/ice_cream_truck

# Format the code with Black
format:
	black ./ice_cream_truck_api/

# Phony target to ensure that the lint and test targets are always run
PHONY: lint test format
