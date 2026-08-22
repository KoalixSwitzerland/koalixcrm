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

# Upload the DocumentTemplate assets the DB already points at into object
# storage. `minio-setup` only creates the bucket, so on a fresh stack (or a DB
# carried over from the filesystem-era install) the PDF worker dies with
# 404 .../koalixcrm-pdf-exports/templates/xsl/invoice.xsl. Idempotent: objects
# that already exist are skipped. Non-fatal — a seeding problem should not stop
# the whole dev stack from coming up, and the command reports what it could not
# resolve.
python manage.py seed_document_template_files || \
    echo "WARNING: template seeding failed — PDF export may 404 on templates/" >&2

# Compile gettext message catalogs (.po -> .mo). Done at startup rather than
# image build because the source tree (incl. the .po files) is bind-mounted
# over the image at runtime, which would shadow any .mo built into the image.
python manage.py compilemessages

python manage.py collectstatic --noinput

# Start Django runserver under debugpy.
# debugpy listens on 0.0.0.0:5678 without blocking startup (no --wait-for-client).
# Attach the PyCharm/IntelliJ debugger at any time after the server starts.
exec python -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
