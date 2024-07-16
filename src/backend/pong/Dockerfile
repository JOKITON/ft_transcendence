# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/14 21:55:03 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 AS builder

LABEL traefik.enable=true
LABEL traefik.http.routers.pong.rule="Host(`localhost`) && PathPrefix(`/api/pong/`)"
LABEL traefik.http.services.pong.loadbalancer.server.port=80

RUN apk add --no-cache && apk update --no-cache \
  && apk add python3 py3-pip curl tzdata shadow sudo \ 
  --no-cache netcat-openbsd zsh

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /pong

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv

COPY pong .

RUN . /opt/venv/bin/activate && pip install -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

COPY /utils/init.sh .

RUN chmod +x init.sh

CMD sh init.sh
