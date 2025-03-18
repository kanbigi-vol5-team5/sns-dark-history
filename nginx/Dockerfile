FROM nginx:latest

RUN rm -f /etc/nginx/conf.d/*
COPY nginx/conf.d/ /etc/nginx/conf.d/
COPY nginx/nginx.conf /etc/nginx/nginx.conf
