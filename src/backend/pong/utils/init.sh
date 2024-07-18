if [ "$DATABASE" = "postgres" ]; then
  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done
fi

python manage.py migrate --noinput

python manage.py flush --no-input

python manage.py makemigrations pong

python manage.py migrate pong

python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:80 config.wsgi:application --reload --timeout 120
