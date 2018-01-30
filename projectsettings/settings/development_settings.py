from .base_settings import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

GRAPPELLI_INDEX_DASHBOARD = 'projectsettings.dashboard.CustomIndexDashboard'