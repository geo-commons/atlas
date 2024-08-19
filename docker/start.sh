#!/usr/bin/env sh
set -e

# Collect static files
python /app/manage.py collectstatic --noinput

# Run migrations
python /app/manage.py migrate

uwsgi --http :8000 \
    --module atlas.wsgi \
    --processes 4 \
    --threads 2 \
    --buffer-size 8192 \
    --static-map /atlas/static=/app/static \
    --static-map /atlas/media=/app/media \
    --static-map /atlas/docs/=/app/docs/user/site \
    --static-map /atlas/admin/docs/=/app/docs/admin/site \
    --static-index index.html
