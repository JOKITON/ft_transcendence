FROM nginx:alpine

RUN apk add openssl --no-cache

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/nginx/certs

RUN openssl req -x509 -out /etc/nginx/certs/localhost.crt -keyout /etc/nginx/certs/localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost'

COPY health-check.sh health-check.sh

RUN chmod +x health-check.sh

CMD ["sh", "health-check.sh"]
