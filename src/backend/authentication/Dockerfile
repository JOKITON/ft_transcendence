# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
#    Updated: 2024/08/26 18:15:06 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM python:alpine3.19

LABEL traefik.enable=true
LABEL traefik.http.routers.authentication.rule="Host(`localhost`) && PathPrefix(`/api/v1`)"
LABEL traefik.http.services.authentication.loadbalancer.server.port=80

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3 py3-pip

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /authentication

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY authentication .

RUN pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
