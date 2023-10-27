# Base image
FROM ubuntu:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    postgresql \
    nginx

# Create and set the working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install project dependencies using Pipenv
RUN pip3 install --no-cache-dir pipenv && \
    pipenv install --system --deploy --ignore-pipfile

# Copy the Django project files to the working directory
COPY ._cream/ice_trucck_api /app/

# Install dotenv package
RUN pipenv install python-dotenv

# Load environment variables from .env file
RUN pipenv run python -m dotenv .env

# Configure PostgreSQL
RUN service postgresql start && \
    su - postgres -c "psql -c 'CREATE DATABASE ${POSTGRES_NAME};'" && \
    su - postgres -c "psql -c \"ALTER USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';\""

# Configure Nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
    rm /etc/nginx/sites-enabled/default && \
    ln -s /app/nginx.conf /etc/nginx/sites-enabled/

# Expose ports
EXPOSE 80

# Start the Django app with Uvicorn
CMD service postgresql start && \
    nginx && \
    pipenv run uvicorn ice_cream_truck_api.asgi:application --host 0.0.0.0 --port 8000
