FROM python:slim-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

# Install required packages
RUN apt-get update && apt-get install -y netcat

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Django project files
COPY . /usr/src/app/

# Copy & give permissions to entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY home/static /home/app/web/static

RUN python manage.py collectstatic --noinput

# Change permissions to allow reading/writing
RUN chmod -R 755 home/static/

# Run the application
CMD ["/usr/src/app/entrypoint.sh"]