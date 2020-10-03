#!/bin/bash

echo "Sleeping for 2s to make sure DB is up and running..."
sleep 2s

# Apply database migrations
echo "Apply database migrations"
python3 manage.py makemigrations orders
python3 manage.py migrate 

echo "running development server"
python3 manage.py runserver 0.0.0.0:8000