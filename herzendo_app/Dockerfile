# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.14-alpine AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /herzendo
COPY ./requirements.txt /herzendo
RUN apk add --no-cache --virtual .build-deps \
      build-base \ 
      cairo-dev \
      freetype-dev \
      gdk-pixbuf-dev \
      harfbuzz-dev \
      jbig2dec-dev \
      jpeg-dev \
      lcms2-dev \
      libffi-dev \
      libxml2-dev \
      libxslt-dev \
      mariadb-dev \
      mupdf-dev \
      musl-dev \
      openjpeg-dev \
      pango-dev \
      pkgconf \
      zlib-dev && \  
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

FROM --platform=$BUILDPLATFORM python:3.14-alpine AS base
WORKDIR /home/herzendo_app/
RUN apk add --no-cache \ 
      ca-certificates \
      cairo \
      curl \
      font-liberation \
      font-opensans \
      fontconfig \
      freetype \
      gdk-pixbuf \
      harfbuzz-dev \
      gumbo-parser-dev \
      jpeg \
      libffi \
      libxml2 \
      libxslt \
      mariadb-connector-c-dev \
      weasyprint \
      zlib && \
      update-ca-certificates

RUN adduser -S -G www-data www-data
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY ./ ./
# Crear los directorios iniciales
RUN mkdir -p /home/herzendo_app/media
# Cambiar los permisos de los archivos copiados
RUN chown -R www-data:www-data /home/herzendo_app/ /home/herzendo_app/media
USER www-data

FROM --platform=$BUILDPLATFORM base AS prod
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/
COPY ./conf/uwsgi/uwsgi.ini /home/herzendo_app/config/uwsgi/uwsgi.ini

FROM --platform=$BUILDPLATFORM base AS debug
RUN pip install --no-cache-dir django-debug-toolbar==6.*
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:8000/ || exit 1