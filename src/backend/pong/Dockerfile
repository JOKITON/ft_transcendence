# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/07 22:37:01 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20

LABEL traefik.enable=true
LABEL traefik.http.routers.pong.rule="Host(`localhost`) && PathPrefix(`/api/v1/pong`)"
LABEL traefik.http.services.pong.loadbalancer.server.port=80 

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3 py3-pip

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /pong

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pong .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip3 install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
