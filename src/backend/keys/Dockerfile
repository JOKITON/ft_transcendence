# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Updated: 2024/09/04 11:15:00 by jaizpuru         ###   ########.fr        #
#    Updated: 2024/09/06 18:23:06 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


FROM alpine:3.20

LABEL traefik.enable=true
LABEL traefik.http.routers.keys.rule="Host(`localhost`) && PathPrefix(`/api/v1/keys`)"
LABEL traefik.http.services.keys.loadbalancer.server.port=80

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /keys

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY keys .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
