#!/bin/sh
# docker/prod/entrypoint.sh
#
# Production entrypoint for docker/prod/Dockerfile.django.
# Runs migrations and collectstatic, then starts Gunicorn.

set -e

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-projectsettings.settings.production_docker_postgres_settings}

python manage.py migrate --noinput || true
python manage.py collectstatic --noinput

exec gunicorn projectsettings.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-120}
