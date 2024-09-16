# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/08 13:24:14 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/16 12:41:30 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 as Builder

LABEL traefik.enable=true
LABEL traefik.http.routers.friendship.rule="Host(`localhost`) && PathPrefix(`/api/v1/friendship`)"
LABEL traefik.http.services.friendship.loadbalancer.server.port=80


RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3 jq
RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /friendship

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY friendship .

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
