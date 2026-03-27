#!/usr/bin/env sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating initial data..."
python manage.py create_initial_data

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
