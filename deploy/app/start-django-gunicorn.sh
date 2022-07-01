#!/usr/bin/env bash

wait-for-it "${EXAMPLE_DB_HOST:-example-database}":5432 -s -t 180 \
&& python /app/src/manage.py migrate --noinput \
&& gunicorn example.asgi:application --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8042
