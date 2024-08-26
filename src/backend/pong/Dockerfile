# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/08/26 18:06:24 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:latest 

LABEL traefik.enable=true
LABEL traefik.http.routers.authentication.rule="Host(`localhost`) && PathPrefix(`/api/pong/`)"
LABEL traefik.http.services.authentication.loadbalancer.server.port=8000
# tu con el proxy puedes exponer o no este contenedor a la red externa, o exponerlo en unhost difernete

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3 py3-pip

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /pong/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip3 install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
