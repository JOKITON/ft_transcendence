FROM alpine:3.20

RUN apk add openssl nginx --no-cache

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/nginx/certs

RUN openssl req -x509 -out /etc/nginx/certs/localhost.crt -keyout /etc/nginx/certs/localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost'

CMD ["nginx", "-g", "daemon off;"]
