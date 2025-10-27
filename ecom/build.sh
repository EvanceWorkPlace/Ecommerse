#!/usr/bin/env bash
# Exit immediately if a command fails
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start gunicorn server
gunicorn ecom.wsgi
