"""
Django settings for koalixcrm project when used in productive environment.
"""

from .base_settings import *

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = bool(os.environ.get("DEBUG", default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "postgres"),
        "USER": os.environ.get("SQL_USER", "postgres"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

FOP_EXECUTABLE = "/usr/bin/fop-2.2/fop/fop"
GRAPPELLI_INDEX_DASHBOARD = 'projectsettings.dashboard.CustomIndexDashboard'
FILEBROWSER_CONVERT_FILENAME = False
KOALIXCRM_REST_API_AUTH = True