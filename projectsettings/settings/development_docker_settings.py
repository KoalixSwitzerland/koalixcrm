"""
Django settings for koalixcrm project in Docker development environment.
Uses PostgreSQL, connects to ElasticMQ/MinIO/Keycloak via docker-compose.
"""

from .base_settings import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'modify_during_deployment')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']

# Database: PostgreSQL in Docker, with SQLite fallback
DB_CHOICE = os.environ.get('DB_CHOICE', 'postgresql')

if DB_CHOICE == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ.get('SQLITE_DB_FILE', os.path.join(BASE_DIR, 'db.sqlite3')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'koalixcrm'),
            'USER': os.environ.get('POSTGRES_USER', 'koalixcrm'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'koalixcrm'),
            'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }

GRAPPELLI_INDEX_DASHBOARD = 'projectsettings.dashboard.CustomIndexDashboard'

KOALIXCRM_REST_API_AUTH = True

# S3 storage for generated PDFs
S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL')
S3_PDF_BUCKET = os.environ.get('S3_PDF_BUCKET', 'koalixcrm-pdf-exports')
# Media and generated PDFs share one bucket locally.
S3_MEDIA_BUCKET = os.environ.get('S3_MEDIA_BUCKET', S3_PDF_BUCKET)
# Endpoint the *browser* uses. Presigned URLs must be signed against this host
# (SigV4 signs Host, so it cannot be rewritten afterwards). Locally the
# container reaches MinIO at http://minio:9000 while the browser needs the
# published port. Unset in production, where the real S3 endpoint serves both.
S3_PUBLIC_ENDPOINT_URL = os.environ.get('S3_PUBLIC_ENDPOINT_URL')
PRESIGNED_DOWNLOAD_URL_EXPIRY = int(os.environ.get('PRESIGNED_DOWNLOAD_URL_EXPIRY', '300'))

# Admin OIDC client (Django admin login via Keycloak)
ADMIN_OIDC_ISSUER = os.environ.get('ADMIN_OIDC_ISSUER')
ADMIN_OIDC_CLIENT_ID = os.environ.get('ADMIN_OIDC_CLIENT_ID')
ADMIN_OIDC_CLIENT_SECRET = os.environ.get('ADMIN_OIDC_CLIENT_SECRET')

# M2M client (Celery workers — client_credentials grant)
CELERY_WORKER_M2M_OIDC_ISSUER = os.environ.get('CELERY_WORKER_M2M_OIDC_ISSUER')
CELERY_WORKER_M2M_CLIENT_ID = os.environ.get('CELERY_WORKER_M2M_CLIENT_ID')
CELERY_WORKER_M2M_CLIENT_SECRET = os.environ.get('CELERY_WORKER_M2M_CLIENT_SECRET')

# SITE_URL for building OAuth callback URLs
SITE_URL = os.environ.get('SITE_URL', '')
