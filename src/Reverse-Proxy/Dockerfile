# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/26 17:07:18 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/14 18:37:28 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM traefik:v3.0 AS Builder

#RUN mkdir -p /certs

#RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#  -subj "/C=ES/ST=Urduliz/L=Madrid/O=42Urduliz/OU=42Urduliz/CN=dugonzal.42.fr" \
#  -keyout /certs/traefik.key  -out /certs/traefik.crt && \
#  chmod 600 /certs/*

#COPY conf/traefik.toml /etc/traefik/
CMD ["traefik", "--api.insecure=true", "--providers.docker=true", "--entrypoints.web.address=:80", "--log.level=DEBUG"]
#CMD ["traefik", "--configfile=/etc/traefik/traefik.toml"]
