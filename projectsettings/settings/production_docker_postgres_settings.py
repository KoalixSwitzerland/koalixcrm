"""
Django settings for koalixcrm project when used in productive environment.
"""

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'modify_during_deployment'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

FOP_EXECUTABLE = "/usr/bin/fop-2.2/fop/fop"
GRAPPELLI_INDEX_DASHBOARD = 'projectsettings.dashboard.CustomIndexDashboard'
FILEBROWSER_CONVERT_FILENAME = False
KOALIXCRM_REST_API_AUTH = True