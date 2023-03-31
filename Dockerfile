FROM python:3.9-alpine
RUN apk add tiff-dev jpeg-dev zlib-dev freetype-dev lcms2-dev libwebp-dev tcl-dev tk-dev libffi-dev
RUN apk add --no-cache --update \
    build-base \
    postgresql-dev \
    bash \
    && rm -rf /var/cache/apk/*

RUN mkdir /core
RUN mkdir /static
WORKDIR /api

COPY requirements.txt /api

RUN pip install --upgrade pip \
    && pip install -r requirements.txt