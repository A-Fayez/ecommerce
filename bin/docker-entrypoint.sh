#!/bin/bash

echo "Sleeping for 2s to make sure DB is up and running..."
sleep 2s

# Collect static files (not deployed yet)
# echo "Collect static files"
# python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

echo "Starting development server at 0.0.0.0:8000"
python3 manage.py runserver 0.0.0.0:8000