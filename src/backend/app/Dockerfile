# Use an official Python runtime as a parent image
FROM python:slim-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install required packages
RUN apt-get update && apt-get install -y netcat

# Install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Django project files
COPY . /usr/src/app/

# Copy & give permissions to entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/
RUN chmod +x /usr/src/app/entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["/usr/src/app/entrypoint.sh"]