#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

# Generate keys for RSA
if [ ! -f /usr/src/app/secrets/jwt_auth_private.pem ]; then
  openssl genpkey -algorithm RSA -out /usr/src/app/secrets/jwt_auth_private.pem -pkeyopt rsa_keygen_bits:2048
fi

if [ ! -f /usr/src/app/secrets/jwt_auth_public.pem ]; then
  openssl rsa -pubout -in /usr/src/app/secrets/jwt_auth_private.pem -out /usr/src/app/secrets/jwt_auth_public.pem
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

# echo "Flushing database..."
# python manage.py flush --no-input

# echo "Creating superuser Joe..."
# python manage.py createsuperuser --username=joe --email=joe@example.com

# Start the Django development server
echo "Starting Django development server..."
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application --reload --timeout 120
