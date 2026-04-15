#!/bin/sh
# docker/dev/entrypoint.sh
#
# Dev entrypoint for docker/dev/Dockerfile.django.
# Runs migrations then starts Django with debugpy listening on port 5678.
#
# IntelliJ/PyCharm: attach a Python Remote Debug configuration to localhost:5678

set -e

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-projectsettings.settings.development_docker_settings}

python manage.py sync_split_migrations
python manage.py migrate --noinput

python manage.py collectstatic --noinput

# Start Django runserver under debugpy.
# debugpy listens on 0.0.0.0:5678 without blocking startup (no --wait-for-client).
# Attach the PyCharm/IntelliJ debugger at any time after the server starts.
exec python -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
