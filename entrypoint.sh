#!/bin/bash

# Install dependencies
pip install -r development_requirements.txt

# Install FOP 2.2
wget https://storage.googleapis.com/server8koalixnet_backup/fop-2.2-bin.tar.gz
tar -xzf fop-2.2-bin.tar.gz -C ../usr/bin
rm -rf fop-2.2-bin.tar.gz
chmod 755 /usr/bin/fop-2.2/fop

# Install Java 8
wget https://storage.googleapis.com/server8koalixnet_backup/jdk-8u181-linux-x64.tar.gz
tar -xzf jdk-8u181-linux-x64.tar.gz -C ../usr/bin
rm -rf jdk-8u181-linux-x64.tar.gz

# Create /media/uploads/ directory which is required by django filebrowser
mkdir -p projectsettings/media/uploads
chmod -R 755 projectsettings/media

# Create /static/pdf for FOP PDF export
mkdir -p projectsettings/static/pdf
chmod -R 755 projectsettings/static/pdf

# Execute startup scripts
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py runserver 0.0.0.0:8000