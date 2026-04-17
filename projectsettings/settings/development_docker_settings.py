"""
Django settings for koalixcrm project in Docker development environment.
Uses PostgreSQL, connects to ElasticMQ/MinIO/Keycloak via docker-compose.
"""

from .base_settings import *  # noqa: F401, F403

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'modify_during_deployment')  # noqa: F405

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')  # noqa: F405

ALLOWED_HOSTS = ['*']

# Database: PostgreSQL in Docker, with SQLite fallback
DB_CHOICE = os.environ.get('DB_CHOICE', 'postgresql')  # noqa: F405

if DB_CHOICE == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ.get('SQLITE_DB_FILE', os.path.join(BASE_DIR, 'db.sqlite3')),  # noqa: F405
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'koalixcrm'),  # noqa: F405
            'USER': os.environ.get('POSTGRES_USER', 'koalixcrm'),  # noqa: F405
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'koalixcrm'),  # noqa: F405
            'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),  # noqa: F405
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),  # noqa: F405
        }
    }

FOP_EXECUTABLE = "/usr/bin/fop-2.9/fop/fop"
GRAPPELLI_INDEX_DASHBOARD = 'projectsettings.dashboard.CustomIndexDashboard'

KOALIXCRM_REST_API_AUTH = True

# S3 storage for generated PDFs
S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL')  # noqa: F405
S3_PDF_BUCKET = os.environ.get('S3_PDF_BUCKET', 'koalixcrm-pdf-exports')  # noqa: F405

# Admin OIDC client (Django admin login via Keycloak)
ADMIN_OIDC_ISSUER = os.environ.get('ADMIN_OIDC_ISSUER')  # noqa: F405
ADMIN_OIDC_CLIENT_ID = os.environ.get('ADMIN_OIDC_CLIENT_ID')  # noqa: F405
ADMIN_OIDC_CLIENT_SECRET = os.environ.get('ADMIN_OIDC_CLIENT_SECRET')  # noqa: F405

# M2M client (Celery workers — client_credentials grant)
CELERY_WORKER_M2M_OIDC_ISSUER = os.environ.get('CELERY_WORKER_M2M_OIDC_ISSUER')  # noqa: F405
CELERY_WORKER_M2M_CLIENT_ID = os.environ.get('CELERY_WORKER_M2M_CLIENT_ID')  # noqa: F405
CELERY_WORKER_M2M_CLIENT_SECRET = os.environ.get('CELERY_WORKER_M2M_CLIENT_SECRET')  # noqa: F405
CELERY_WORKER_M2M_SCOPE = os.environ.get('CELERY_WORKER_M2M_SCOPE')  # noqa: F405

# SITE_URL for building OAuth callback URLs
SITE_URL = os.environ.get('SITE_URL', '')  # noqa: F405
