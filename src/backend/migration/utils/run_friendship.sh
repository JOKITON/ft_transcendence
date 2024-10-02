echo "Getting keys for friendship..."
sh friendship/utils/get_keys.sh

echo "Making migrations for friendship..."
python friendship/manage.py makemigrations friendship --noinput

echo "Running migrations for friendship..."
python friendship/manage.py migrate --noinput
