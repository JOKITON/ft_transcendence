#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

# Check if the directory for keys exists, if not, create it
if [ ! -d /keys/secrets ]; then
  echo "Creating /keys/secrets directory..."
  mkdir -p /keys/secrets
fi
# Check if the private key exists, if not, generate it
if [ ! -f /keys/secrets/private.pem ]; then
  echo "Generating private key..."
  openssl genrsa -out /keys/secrets/private.pem 2048

  # Verify if the private key was successfully created
  if [ -f /keys/secrets/private.pem ]; then
    echo "Private key generated successfully"
  else
    echo "Failed to generate private key"
    exit 1
  fi
else
  echo "Private key already exists"
fi

# Check if the public key exists, if not, generate it
if [ ! -f /keys/secrets/public.pem ]; then
  echo "Generating public key..."
  openssl rsa -in /keys/secrets/private.pem -pubout -out /keys/secrets/public.pem

  # Verify if the public key was successfully created
  if [ -f /keys/secrets/public.pem ]; then
    echo "Public key generated successfully"
  else
    echo "Failed to generate public key"
    exit 1
  fi
else
  echo "Public key already exists"
fi

# Start the Django development server
echo "Starting Django development server..."
gunicorn --bind 0.0.0.0:80 config.wsgi:application --reload --timeout 120
