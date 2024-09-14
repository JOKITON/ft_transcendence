# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/05 20:54:09 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/07 23:55:19 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3:20 as Builder

LABEL traefik.enable=true
LABEL traefik.http.routers.LiveGameSession.rule="Host(`localhost`) && PathPrefix(`/api/v1/live`)"
LABEL traefik.http.service.LiveGameSession.loadbalancer.server.port=80

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /LiveGameSession

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY LiveGameSession .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
