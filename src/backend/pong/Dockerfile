# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/27 16:36:14 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Use a more specific base image with Python pre-installed
FROM alpine:3.20 as builder

LABEL traefik.enable=true
LABEL traefik.http.routers.authentication.rule="Host(`localhost`) && PathPrefix(`/api/pong/`)"
LABEL traefik.http.services.authentication.loadbalancer.server.port=8000

# Install system dependencies
RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3

# Set timezone
RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

# Set the working directory in the container
WORKDIR /usr/src/app/

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN python -m venv /opt/venv && \
  . /opt/venv/bin/activate && \
  pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# Start the entrypoint script
CMD ["sh", "utils/init.sh"]
