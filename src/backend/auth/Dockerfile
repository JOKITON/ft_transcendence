# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/21 13:32:06 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 AS builder

LABEL traefik.enable=true
LABEL traefik.http.routers.autentication.rule="Host(`localhost`) && PathPrefix(`/api/token/`)"
LABEL traefik.http.services.autentication.loadbalancer.server.port=8000

RUN apk add --no-cache \
    curl \
    tzdata \
    shadow \
    sudo \
    openssl \
    netcat-openbsd \
    python3 \
    zsh && \
    cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

# Set the working directory in the container
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy and install Python dependencies
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# Ensure the secrets directory exists
RUN mkdir -p /usr/src/app/secrets

# Copy your Django project files
COPY . /usr/src/app/

# Copy & give permissions to entrypoint.sh
COPY ./utils/init.sh /usr/src/app/
RUN chmod +x /usr/src/app/init.sh

# Expose port 8000
EXPOSE 8000

CMD ["sh", "/usr/src/app/init.sh"]