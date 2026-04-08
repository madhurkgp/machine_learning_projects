#!/bin/bash

# Production Deployment Script for IMDB Rating Predictor
# This script prepares the application for production deployment

set -e

echo "Starting production deployment..."

# Set environment variables
export DEBUG=False
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
export SECRET_KEY="your-secret-key-here"

# Install production dependencies
pip install gunicorn whitenoise

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create superuser if needed (uncomment and modify)
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell

# Start gunicorn server
gunicorn imdb_project.wsgi:application --bind 0.0.0.0:8000

echo "Deployment complete!"
