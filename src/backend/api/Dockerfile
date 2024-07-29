# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/29 09:31:46 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Use a more specific base image with Python pre-installed
FROM python:3.12-alpine as builder

LABEL traefik.enable=true
LABEL traefik.http.routers.authentication.rule="Host(`localhost`) && PathPrefix(`/api/user/`)"
LABEL traefik.http.services.authentication.loadbalancer.server.port=8000

# Install system dependencies
RUN apk add --no-cache \
    curl \
    tzdata \
    shadow \
    sudo \
    openssl \
    netcat-openbsd \
    zsh

# Set timezone
RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

# Set the working directory in the container
WORKDIR /usr/src/app/

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy and install Python dependencies
COPY utils/requirements.txt .
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# Copy the Django project files
COPY . /usr/src/app/

# Copy and set permissions for the entrypoint script
COPY ./utils/init.sh /usr/src/app/
RUN chmod +x /usr/src/app/init.sh

# Expose port 8000
EXPOSE 8000

# Start the entrypoint script
CMD ["sh", "/usr/src/app/init.sh"]
