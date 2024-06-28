#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL to start..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL is up and running"
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Flushing database..."
python manage.py flush --no-input

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000