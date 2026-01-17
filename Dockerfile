# syntax=docker/dockerfile:1
FROM python:3.12-slim

ARG APP_ENV=development
ARG APP_VERSION=dev
ARG GIT_SHA=unknown

ENV APP_ENV=${APP_ENV} \
    APP_VERSION=${APP_VERSION} \
    GIT_SHA=${GIT_SHA} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

LABEL org.opencontainers.image.title='keylog_heatmap' \
      org.opencontainers.image.version='${APP_VERSION}' \
      org.opencontainers.image.revision='${GIT_SHA}' \
      org.opencontainers.image.description='Keyboard heatmap merge+render container'

WORKDIR /app

# install deps
RUN pip install --no-cache-dir pillow

# copy code and assets
COPY heatmap ./heatmap
COPY main.py reset_keyfreq.py ./

# default command: merge + render
CMD ["python", "main.py"]