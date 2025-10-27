#!/bin/bash
set -e

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server
exec gunicorn ecom.wsgi --bind 0.0.0.0:$PORT
