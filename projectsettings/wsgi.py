"""
WSGI config for koalixcrm project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named `application`. Django's `runserver` and `runfcgi` commands discover
this application via the `WSGI_APPLICATION` setting.

Usually this will be called "koalixcrm.wsgi".
"""

import os
from django.core.wsgi import get_wsgi_application

# The settings module that Django uses. By convention, it is usually in the form "myproject.settings.production"
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "koalixcrm.projectsettings.settings.production_docker_postgres_settings")

application = get_wsgi_application()