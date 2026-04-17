"""
Django settings for koalixcrm project when used in development environment.
"""

from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'modify_during_deployment'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

FOP_EXECUTABLE = "/usr/bin/fop-2.9/fop/fop"
GRAPPELLI_INDEX_DASHBOARD = 'projectsettings.dashboard.CustomIndexDashboard'

KOALIXCRM_REST_API_AUTH = True
