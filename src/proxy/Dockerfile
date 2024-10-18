FROM nginx:alpine

RUN apk add openssl

# Change configuration for Nginx
COPY nginx.conf /etc/nginx/nginx.conf
# COPY default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/certs

RUN openssl req -x509 -out /etc/nginx/certs/localhost.crt -keyout /etc/nginx/certs/localhost.key \
-newkey rsa:2048 -nodes -sha256 \
-subj '/CN=localhost'

CMD ["nginx", "-g", "daemon off;"]