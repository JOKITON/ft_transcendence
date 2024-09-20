# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/05 20:54:09 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/20 13:36:48 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3:20 as builder 
# mas adelante con el builder podriamos en una imagen posterior compilar el codigo para distribuirlo

LABEL traefik.enable=true
LABEL traefik.http.routers.LiveGameSession.rule="Host(`localhost`) && PathPrefix(`/api/v1/live`)"
LABEL traefik.http.service.LiveGameSession.loadbalancer.server.port=80

RUN apk add --no-cache \
    curl \
    tzdata \
    shadow \
    sudo \
    openssl \
    netcat-openbsd \
    python3 \
    zsh && \
    cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime

WORKDIR /LiveGameSession

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY LiveGameSession .

RUN python -m venv /opt/venv && source /opt/venv/bin/activate \
  && pip install --no-cache-dir -r utils/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# Ensure the secrets directory exists
RUN mkdir -p /usr/src/app/secrets

# Copy your Django project files
COPY keys /usr/src/app/

# Copy & give permissions to entrypoint.sh
COPY keys/utils/init.sh /usr/src/app/
RUN chmod +x /usr/src/app/init.sh

# Expose port 8000
EXPOSE 8000

CMD ["sh", "/usr/src/app/init.sh"]