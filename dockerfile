# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV APP_ENV=development \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# install deps
RUN pip install --no-cache-dir pillow pynput

# copy code and assets
COPY heatmap ./heatmap
COPY main.py reset_keyfreq.py ./

# default command: merge + render
CMD ["python", "main.py"]