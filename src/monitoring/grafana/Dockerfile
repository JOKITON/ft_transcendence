# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/26 18:57:05 by Dugonzal          #+#    #+#              #
#    Updated: 2024/08/26 18:03:26 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:latest AS Builder

LABEL traefik.enable=true
LABEL traefik.http.routers.grafana.rule=Host(`grafana.localhost`)
LABEL traefik.http.services.grafana.loadbalancer.server.port=3000

RUN apk update --update && apk upgrade --no-cache && apk add grafana --no-cache

# Copy custom configuration
COPY grafana.ini /usr/share/grafana/conf/grafana.ini

COPY  provisioning /usr/share/grafana/conf/provisioning

# COPY provisioning/dashboards/ /usr/share/grafana/conf/provisioning/
CMD grafana-server --homepath=/usr/share/grafana
