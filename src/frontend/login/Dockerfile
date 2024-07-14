# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Dugonzal <dugonzal@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/25 20:40:21 by Dugonzal          #+#    #+#              #
#    Updated: 2024/07/14 17:05:15 by Dugonzal         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20 AS builder


RUN apk update && apk add --no-cache nodejs npm

WORKDIR /login

COPY login/ .

RUN npm install

CMD npm run serve -- --port 80 
