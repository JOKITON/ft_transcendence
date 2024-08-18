# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/25 20:40:21 by Dugonzal          #+#    #+#              #
#    Updated: 2024/08/16 22:53:29 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM node:18-alpine AS builder

LABEL traefik.enable=true
LABEL traefik.http.routers.vue.rule="Host(`localhost`) && PathPrefix(`/`)"
LABEL traefik.http.services.vue.loadbalancer.server.port=80

WORKDIR /vue-project

COPY vue-project/package*.json ./
RUN npm install

COPY vue-project ./
RUN npm update vite

EXPOSE 80

CMD ["npm", "run", "dev", "--", "--host", "--port", "80"]
