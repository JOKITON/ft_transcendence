# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/08 13:24:14 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/14 13:08:56 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 as builder

LABEL traefik.enable=true
LABEL traefik.http.routers.friendship.rule="Host(`localhost`) && PathPrefix(`/api/v1/friendship`)"
LABEL traefik.http.services.friendship.loadbalancer.server.port=80


RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3 jq
RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /friendship

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY friendship .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
