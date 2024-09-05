# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/09 16:13:42 by Dugonzal          #+#    #+#              #
<<<<<<< Updated upstream:src/backend/authentication/Dockerfile
#    Updated: 2024/09/04 11:18:50 by jaizpuru         ###   ########.fr        #
=======
#    Updated: 2024/09/05 18:53:36 by jaizpuru         ###   ########.fr        #
>>>>>>> Stashed changes:src/backend/auth/Dockerfile
#                                                                              #
# **************************************************************************** #

FROM python:alpine3.20

LABEL traefik.enable=true
LABEL traefik.http.routers.auth.rule="Host(`localhost`) && PathPrefix(`/api/v1`)"
LABEL traefik.http.services.auth.loadbalancer.server.port=80

RUN apk add --no-cache curl tzdata shadow openssl netcat-openbsd zsh python3 py3-pip

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /usr/src/app/auth

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY auth .

RUN pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["zsh", "utils/init.sh"]
