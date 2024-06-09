FROM python:slim-bullseye

EXPOSE 8000

# Install required packages
RUN apt-get update && apt-get install -y postgresql-client

# Set the working directory in the container
WORKDIR /usr/src/app/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Django project files
COPY . /usr/src/app/
# Ensure the static files are collected (if needed)
RUN python manage.py collectstatic --noinput

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]