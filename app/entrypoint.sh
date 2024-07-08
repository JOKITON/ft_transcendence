#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL to start..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL is up and running"
fi

python --version

# Generate keys for RSA
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private.pem -out public.pem

# echo "Creating superuser Joe..."
# python manage.py createsuperuser --username=joe --email=joe@example.com

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Flushing database..."
python manage.py flush --no-input

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000