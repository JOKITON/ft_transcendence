echo "Getting keys for pong..."
sh pong/utils/get_keys.sh

echo "Making migrations for pong..."
python pong/manage.py makemigrations pong --noinput

echo "Running migrations for pong..."
python pong/manage.py migrate --noinput
