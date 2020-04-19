#!/usr/bin/env bash
HTML=${PWD}
echo $HTML
docker stop ph2docs-nginx
docker rm ph2docs-nginx
docker run --name ph2docs-nginx -v $HTML:/usr/share/nginx/html:ro -v $HTML/scripts/nginx.conf:/etc/nginx/nginx.conf:ro -p 8008:80 -d nginx
echo docs at localhost:8008
docker logs --follow ph2docs-nginx
docker stop ph2docs-nginx
docker rm ph2docs-nginx
