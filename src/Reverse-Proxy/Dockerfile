# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/26 17:07:18 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/10 17:51:09 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 AS Builder

RUN apk update && apk upgrade --no-cache  \
  && apk add zsh openssl traefik ca-certificates --no-cache

#RUN mkdir -p /certs

#RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#  -subj "/C=ES/ST=Urduliz/L=Madrid/O=42Urduliz/OU=42Urduliz/CN=dugonzal.42.fr" \
#  -keyout /certs/traefik.key  -out /certs/traefik.crt && \
#  chmod 600 /certs/*

COPY conf/traefik.toml /etc/traefik/

CMD ["traefik", "--configfile=/etc/traefik/traefik.toml"]
