# -*- coding: utf-8 -*-
# Django settings for koalixcrm project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'koalixcrm'             # Or path to database file if using sqlite3.
DATABASE_USER = 'koalixcrm'             # Not used with sqlite3.
DATABASE_PASSWORD = 'koalix5crm1234'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DATE_FORMAT = 'j M Y'
DATETIME_FORMAT = 'j M Y G:i' 
MONTH_DAY_FORMAT = 'j F'
TIME_FORMAT = 'G:i'
YEAR_MONTH_FORMAT = 'F Y'
TIME_ZONE = 'Europe/Zurich'

LANGUAGE_CODE = 'de'

LANGUAGES = (
  ('de', 'German'),
  ('en', 'English'),
)
LOCALE_PATHS = ('crm/locale', 'accounting/locale')

SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = '/var/www/koalixcrm/media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '+d37i!a)&736a^mxykah*l#68)^$4(6ikgbx%4(+1$l98(ktv*'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middleware.threadlocals.ThreadLocals',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    '/var/www/koalixcrm/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'accounting',
    'djangoUserExtention',
    'crm',
    'filebrowser',
    'tinymce',
    'grappelli',
    'django.contrib.admin',
)
