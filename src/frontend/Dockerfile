# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/25 20:40:21 by Dugonzal          #+#    #+#              #
#    Updated: 2024/10/31 00:23:29 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM alpine:3.20

RUN apk add --no-cache nodejs npm

WORKDIR /frontend

COPY frontend .

RUN npm i vite -g

RUN npm i

# RUN npm run type-check

# RUN npm run build

CMD npm run dev

# CMD ["sleep", "1000000"]
# CMD vite preview --port 80
