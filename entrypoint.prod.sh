#!/bin/bash

# Install dependencies
pip install -r base_requirements.txt

# Install FOP 2.2
wget http://archive.apache.org/dist/xmlgraphics/fop/binaries/fop-2.2-bin.tar.gz
tar -xzf fop-2.2-bin.tar.gz -C ../usr/bin
rm -rf fop-2.2-bin.tar.gz
chmod 755 ../usr/bin/fop-2.2/fop

# Install Java 8
wget --no-check-certificate -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u162-b12/0da788060d494f5095bf8624735fa2f1/jdk-8u162-linux-x64.tar.gz
tar -xzf jdk-8u162-linux-x64.tar.gz -C ../usr/bin
rm -rf jdk-8u162-linux-x64.tar.gz

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