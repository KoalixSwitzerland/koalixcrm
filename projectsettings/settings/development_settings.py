from .base_settings import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

GRAPPELLI_INDEX_DASHBOARD = 'projectsettings.dashboard.CustomIndexDashboard'

GRAPPELLI_ADMIN_TITLE = 'JLSCom'

ASYNC_SIGNALS = False
CELERY_BROKER_URL = 'memory://'
RABBITMQ_SIGNALS_BROKER_URL = 'amqp://localhost:5672'
if ASYNC_SIGNALS:
    CELERY_BROKER_URL = RABBITMQ_SIGNALS_BROKER_URL
    CELERY_RESULT_BACKEND = RABBITMQ_SIGNALS_BROKER_URL
CELERY_TASK_ALWAYS_EAGER = False if ASYNC_SIGNALS else True
CELERY_TASK_IGNORE_RESULT = False if ASYNC_SIGNALS else True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', 'pickle']