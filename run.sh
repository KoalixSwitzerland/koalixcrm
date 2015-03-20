#!/usr/bin/env bashchm
pip install -r requirements.txt
python manage.py createinitialrevisions
python manage.py migrate
python manage.py runserver 0.0.0.0:8000