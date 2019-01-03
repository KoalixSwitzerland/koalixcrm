#!/bin/bash

python manage.py migrate --settings=projectsettings.settings.docker_production_settings
python manage.py runserver 0.0.0.0:8000 --settings=projectsettings.settings.docker_production_settings