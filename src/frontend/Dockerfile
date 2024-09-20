# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/25 20:40:21 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/20 13:37:05 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM node:alpine3.20

LABEL traefik.enable=true
LABEL traefik.http.routers.frontend.rule="Host(`localhost`) && PathPrefix(`/`)"
LABEL traefik.http.services.frontend.loadbalancer.server.port=80

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm update vite

RUN npm i && npm update
 
CMD npm  run dev -- --host
