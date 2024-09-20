# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/09 15:44:01 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/04 11:15:23 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20.2

LABEL traefik.enable=true
LABEL traefik.http.routers.prometheus.rule=Host(`prometheus.localhost`)
LABEL traefik.http.services.prometheus.loadbalancer.server.port=9090

RUN apk update --no-cache  \
  && apk upgrade --no-cache && apk add  prometheus --no-cache

COPY conf/prometheus.yml /etc/prometheus/prometheus.yml

CMD prometheus --config.file=/etc/prometheus/prometheus.yml
