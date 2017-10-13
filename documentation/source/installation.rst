.. highlight:: rst

koalixcrm Installation
======================
on Windows 10 Version 1703
---------------------------
Install Python 3.6.2
^^^^^^^^^^^^^^^^^^^^
    Download from https://www.python.org/downloads/
    Install python with the defaults

Install FOP 2.2
^^^^^^^^^^^^^^^
    Download and install java from oracle website
    Download fop2.2 from apache fop website and install

Install koalixcrm app
^^^^^^^^^^^^^^^^^^^^^
    Run command
    C:\Users\YourUser\AppData\Local\Programs\Python\Python36-32\Scripts\pip.exe install koalix-crm

Setup django project
^^^^^^^^^^^^^^^^^^^^
    Run command
    C:\Users\YourUser\AppData\Local\Programs\Python\Python36-32\Scripts\django-admin.exe startproject test_koalixcrm
    mkdir test_koalixcrm\media
    mkdir test_koalixcrm\media\uploads

on ubuntu 17.04
---------------
Install required programs on your ubuntu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    sudo bash
    apt-get install fop virtualenv python3.5
    exit

Create a virtual python environment for the koalixcrm project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    mkdir ~/test_koalixcrm_env
    virtualenv --no-site-package --python=/usr/bin/python3.5 ~/test_koalixcrm_env
    source /test_koalixcrm_env/bin/activate
    pip install koalix-crm

Create a generic django project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    cd ~
    django-admin startproject test_koalixcrm

Common on all Operating Systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Import koalixcrm to your project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Open the file  called settings.py

    Search in the file the variable definition "INSTALLED_APPS"
    Add following lines to the at the end of INSTALLED_APPS:
    'koalixcrm.crm',
    'koalixcrm.accounting',
    'koalixcrm.djangoUserExtension',
    'koalixcrm.subscriptions',
    'filebrowser'

    Create a new variable defintion "KOALIXCRM_PLUGIN"
    KOALIXCRM_PLUGINS = (
        'koalixcrm.subscriptions',
    )

    At the very end of the seetings.py file add the following lines:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, '')

    PROJECT_ROOT = BASE_DIR

    # Settings specific for koalixcrm
    PDF_OUTPUT_ROOT = os.path.join(STATIC_ROOT, 'pdf/')
    FOP_

    # Settings specific for filebrowser
    FILEBROWSER_DIRECTORY = 'uploads/'

Enable the customized additional view for filebrowser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Open the file  called urls.py
Completely rewrite the file with following content

    from django.conf.urls.static import *
    from django.contrib.staticfiles.urls import static
    from django.contrib import admin
    from filebrowser.sites import FileBrowserSite
    from django.core.files.storage import DefaultStorage

    site = FileBrowserSite(name="filebrowser", storage=DefaultStorage())
    customsite = FileBrowserSite(name='custom_filebrowser', storage=DefaultStorage())
    customsite.directory = "uploads/"


    admin.autodiscover()

    urlpatterns = [
        url(r'^admin/filebrowser/', customsite.urls),
        url(r'^admin/', admin.site.urls),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

Afterwards start the django application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    cd ~/test_koalixcrm
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver 127.0.0.1:8000

Log in to the admin website
^^^^^^^^^^^^^^^^^^^^^^^^^^^

What you want to do next is of cause the test the software. Visit your http://127.0.0.1:8000/admin, log in and start testing.

