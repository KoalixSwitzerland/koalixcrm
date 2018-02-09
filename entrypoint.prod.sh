#!/bin/bash

# Install dependencies
pip install -r base_requirements.txt

# Install FOP 2.2
wget https://archive.apache.org/dist/xmlgraphics/fop/source/fop-2.2-src.tar.gz
tar -xzf fop-2.2-src.tar.gz -C ../usr/bin
rm -rf fop-2.2-src.tar.gz

# Execute startup scripts
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000