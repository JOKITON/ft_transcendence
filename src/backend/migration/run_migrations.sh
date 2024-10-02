#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
fi

pwd

#! May be necessary to install dependencies into the container for 'UserModel'

echo "Getting keys for auth..."
sh auth/utils/get_keys.sh

python auth/manage.py showmigrations

echo "Making migrations for auth..."
python auth/manage.py makemigrations UserModel --noinput

echo "Running migrations for auth..."
python auth/manage.py migrate --noinput

echo "Making migrations for auth..."
python auth/manage.py makemigrations authentication --noinput

echo "Running migrations for auth..."
python auth/manage.py migrate --noinput

echo "Getting keys for pong..."
sh pong/utils/get_keys.sh

echo "Making migrations for pong..."
python pong/manage.py makemigrations pong --noinput

echo "Running migrations for pong..."
python pong/manage.py migrate --noinput

echo "Getting keys for friendship..."
sh friendship/utils/get_keys.sh

echo "Making migrations for friendship..."
python friendship/manage.py makemigrations friendship --noinput

echo "Running migrations for friendship..."
python friendship/manage.py migrate --noinput

python auth/manage.py showmigrations

# Add more apps as needed

while :; do sleep 2073600; done