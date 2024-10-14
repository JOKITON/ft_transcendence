# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/05 20:54:09 by Dugonzal          #+#    #+#              #
#    Updated: 2024/10/14 19:33:06 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20


LABEL traefik.enable=true
LABEL traefik.http.routers.livechat.rule="Host(`localhost`) && PathPrefix(`/api/v1/livechat`)"
LABEL traefik.http.services.livechat.loadbalancer.server.port=80

# Middlewares para WebSocket y eliminación del prefijo
LABEL traefik.http.middlewares.websocket-headers.headers.customrequestheaders.Upgrade=websocket
LABEL traefik.http.middlewares.websocket-headers.headers.customrequestheaders.Connection=Upgrade
LABEL traefik.http.middlewares.strip-prefix.stripprefix.prefixes=/api/v1/livechat

# Asociar los middlewares al router
LABEL traefik.http.routers.livechat.middlewares=strip-prefix,websocket-headers
RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3 jq

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /livechat

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY livechat .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
