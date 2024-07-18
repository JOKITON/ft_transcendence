# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/09 15:44:01 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/10 17:51:30 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 AS builder

LABEL traefik.enable=true
LABEL traefik.http.routers.prometheus.rule=Host(`prometheus.localhost`)
LABEL traefik.http.services.prometheus.loadbalancer.server.port=9090

RUN apk update --no-cache  \
  && apk upgrade --no-cache && apk add  prometheus --no-cache

COPY conf/prometheus.yml /etc/prometheus/prometheus.yml

CMD prometheus --config.file=/etc/prometheus/prometheus.yml
