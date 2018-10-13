# -*- coding: utf-8 -*-

from .base_settings import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

FOP_EXECUTABLE = "/usr/bin/fop-2.2/fop/fop"
GRAPPELLI_INDEX_DASHBOARD = 'projectsettings.dashboard.CustomIndexDashboard'

KOALIXCRM_REST_API_AUTH = True
