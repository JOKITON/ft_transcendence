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

python auth/manage.py showmigrations
