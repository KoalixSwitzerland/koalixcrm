# -*- coding: utf-8 -*-
# Django settings for koalixcrm project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'koalixcrm',                      # Or path to database file if using sqlite3.
        'USER': 'koalixcrm',                      # Not used with sqlite3.
        'PASSWORD': 'koalix5crm1234',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Zurich'

LANGUAGE_CODE = 'en'

LANGUAGES = (
  ('de', 'German'),
  ('en', 'English'),
)
LOCALE_PATHS = ('crm/locale', 'accounting/locale', 'subscriptions/locale', 'djangoUserExtension/locale')

SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = '/var/www/koalixcrm/media/'
PROJECT_ROOT = '/var/www/koalixcrm/'
MEDIA_URL = '/media/'
PDF_OUTPUT_ROOT = '/var/www/koalixcrm/media/pdf/'

STATIC_ROOT = '/var/www/koalixcrm//static/'

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"
LOGIN_REDIRECT_URL = '/admin/'

SECRET_KEY = '+d37i!a)&736a^mxykah*l#68)^$4(6ikgbx%4(+1$l98(ktv*'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

TEMPLATE_DIRS = (
    '/var/www/koalixcrm/templates'
)

KOALIXCRM_PLUGINS = (
    'subscriptions',
)

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounting',
    'djangoUserExtension',
    'crm',
    'subscriptions',
    'django.contrib.admin',
    'south'
)
