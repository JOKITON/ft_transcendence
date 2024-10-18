# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/25 20:40:21 by Dugonzal          #+#    #+#              #
#    Updated: 2024/10/17 16:22:58 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20

RUN apk add --no-cache nodejs npm

WORKDIR /frontend

COPY frontend .

RUN npm i

CMD npm  run dev -- --host
