FROM nginx:alpine

# Change configuration for Nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy static files into container
COPY staticfiles /home/app/web/staticfiles

# Change permissions to allow reading/writing
RUN chmod -R 755 /home/app/web/staticfiles

CMD ["nginx", "-g", "daemon off;"]
