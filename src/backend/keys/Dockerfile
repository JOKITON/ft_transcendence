# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/30 00:13:17 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 AS builder

LABEL traefik.enable=true
LABEL traefik.http.routers.autentication.rule="Host(`localhost`) && PathPrefix(`/api/key/`)"
LABEL traefik.http.services.autentication.loadbalancer.server.port=80

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd python3 zsh \
  && cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /keys

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN python -m venv /opt/venv &&  source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir -p secrets


CMD ["sh", "utils/init.sh"]
