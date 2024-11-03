FROM alpine:3.20

RUN apk add --no-cache nodejs npm

WORKDIR /frontend

COPY frontend .

RUN npm i && npm i -g http-server-spa

RUN npm run build-only

CMD http-server-spa ./dist index.html 80