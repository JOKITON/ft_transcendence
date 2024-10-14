# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/24 18:21:25 by Dugonzal          #+#    #+#              #
#    Updated: 2024/10/07 21:37:27 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM redis:7.4-alpine3.20

#LABEL traefik.enable=true
#LABEL traefik.http.routers.livechat.rule="Host(`localhost`)  && PathPrefix(`/api/v1/redis`)"
#LABEL traefik.http.services.livechat.loadbalancer.server.port=80
#COPY redis.conf /usr/local/etc/redis/redis.conf

CMD redis-server
