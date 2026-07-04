"""
Django base settings for koalixcrm project.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application version.
# CI injects this via the KOALIXCRM_VERSION env var (set from the docker
# ARG APP_VERSION at image build time). Local runs without that env fall back
# to a clearly non-release placeholder so they can't be mistaken for a build.
KOALIXCRM_VERSION = os.getenv("KOALIXCRM_VERSION", "vX.Y.Z-develop")

# Application definition
PREREQUISITE_APPS = [
    'django.contrib.contenttypes',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'storages',
]

PROJECT_APPS = [
    'koalixcrm.core',
    'koalixcrm.contacts',
    'koalixcrm.products',
    'koalixcrm.stock',
    'koalixcrm.contracts',
    'koalixcrm.reporting',
    'koalixcrm.accounting',
    'koalixcrm.djangoUserExtension',
    'koalixcrm.subscriptions',
]

INSTALLED_APPS = PREREQUISITE_APPS + PROJECT_APPS

KOALIXCRM_PLUGINS = (
    'koalixcrm.subscriptions',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'koalixcrm.core.middleware.workspace_context.WorkspaceContextMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'koalixcrm.core.middleware.timezoneMiddleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'projectsettings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # koalixcrm.core templates override grappelli admin templates.
            os.path.join(BASE_DIR, 'koalixcrm', 'core', 'templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'koalixcrm.core.context_processors.workspace_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'projectsettings.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = os.environ.get('KOALIXCRM_LANGUAGE_CODE', 'en-us')
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PROJECT_ROOT = BASE_DIR

# Settings specific for koalixcrm
PDF_OUTPUT_ROOT = os.path.join(STATIC_ROOT, 'pdf')

# Settings specific for filebrowser
FILEBROWSER_DIRECTORY = 'uploads/'
FILEBROWSER_EXTENSIONS = {
    'XML': ['.xml'],
    'XSL': ['.xsl'],
    'JPG': ['.jpg'],
    'PNG': ['.png'],
    'GIF': ['.gif'],
    'TTF': ['.ttf'],
}

LOGIN_URL = "/auth/login/"

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'koalixcrm.auth.m2m_authentication.CeleryWorkerM2MAuthentication',
        'koalixcrm.auth.oidc_token_authentication.OIDCAccessTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'koalixcrm API',
    'DESCRIPTION': 'koalixcrm REST API — per-app, versioned, workspace-scoped.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# OIDC Configuration (from environment variables)
OIDC_ISSUER = os.environ.get('OIDC_ISSUER')
OIDC_ACCEPTED_AUDIENCES = [
    aud.strip() for aud in
    os.environ.get('OIDC_ACCEPTED_AUDIENCES', '').split(',')
    if aud.strip()
]

AUTHENTICATION_BACKENDS = [
    'koalixcrm.auth.oidc_backend.OIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]
