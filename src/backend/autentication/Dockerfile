# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/15 15:37:48 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 AS builder

LABEL traefik.enable=true
LABEL traefik.http.routers.autentication.rule="Host(`localhost`) && PathPrefix(`/api`)"
LABEL traefik.http.services.autentication.loadbalancer.server.port=80

RUN apk add --no-cache && apk update --no-cache \
  && apk add python3 py3-pip curl tzdata shadow sudo openssl \ 
  --no-cache netcat-openbsd zsh

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /authentication

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv

COPY autentication .

RUN . /opt/venv/bin/activate && pip install -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

COPY /utils/init.sh .

RUN chmod +x init.sh

CMD sh init.sh
