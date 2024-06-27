# ./vue/Dockerfile
FROM node:22 as build

WORKDIR /app

COPY ./vue-project/package*.json ./

RUN npm install

COPY ./vue-project/ .

RUN npm run build

FROM nginx:alpine

# Copy build output from Stage 1
COPY --from=build /app/dist /home/app/web/static

# Nginx configuration (optional: use if customizing Nginx config)
# COPY ./vue/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]