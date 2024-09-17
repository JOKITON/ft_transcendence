# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/25 20:40:21 by Dugonzal          #+#    #+#              #
#    Updated: 2024/09/06 16:49:35 by jaizpuru         ###   ########.fr        #
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

EXPOSE 80

CMD ["npm", "run", "dev", "--", "--host", "--port", "80"]
