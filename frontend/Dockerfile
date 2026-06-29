FROM nginx:alpine

ENV PORT=8080 \
    API_URL=http://localhost:8000

COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/

CMD sed -i 's/listen[: ]*80;/listen '"$PORT"';/' /etc/nginx/conf.d/default.conf \
    && sed -i 's|__API_URL__|'"$API_URL"'|g' /usr/share/nginx/html/index.html \
    && nginx -g 'daemon off;'
