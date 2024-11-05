FROM nginx:alpine

RUN apk add openssl bash curl --no-cache

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/nginx/certs

RUN openssl req -x509 -out /etc/nginx/certs/localhost.crt -keyout /etc/nginx/certs/localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost'

RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh

RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "auth:80", "--", "./wait-for-it.sh", "pong:80", "--", "./wait-for-it.sh", "friendship:80", "--", "nginx", "-g", "daemon off;"]
