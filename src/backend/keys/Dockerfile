# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/08/26 18:16:52 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:latest

LABEL traefik.enable=true
LABEL traefik.http.routers.keys.rule="Host(`localhost`) && PathPrefix(`/api/v1/keys`)"
LABEL traefik.http.services.keys.loadbalancer.server.port=80

RUN apk add --no-cache gcc curl tzdata shadow openssl netcat-openbsd zsh python3 py3-pip

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /keys

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY authentication .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip3 install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
