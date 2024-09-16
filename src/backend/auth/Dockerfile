# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/16 19:37:33 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 as Builder

LABEL traefik.enable=true
LABEL traefik.http.routers.authentication.rule="Host(`localhost`) && PathPrefix(`/api/v1/auth`)"
LABEL traefik.http.services.authentication.loadbalancer.server.port=80

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /auth

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY auth .

ENV PATH="/opt/venv/bin:$PATH"

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r utils/requirements.txt

CMD ["zsh", "utils/init.sh"]
# CMD ["sleep", "infinity"]
