.. highlight:: rst

************
Installation
************

.. note::
    This version is not recommended for productive use. Therefore productive installation is not yet mentioned in this documentation.

.. contents::


Common Package Requirements
===========================

Following requirements are common for both, development and demo installation of Koalix CRM.

Please install the following packages:

    - Python 2.7 (other versions currently not working, sorry)
    - Django 1.7
    - Mezzanine>=3.1.10
    - po-localization
    - django-bootstrap3
    - django-braces
    - django-import-export
    - django-fsm
    - django-extra-views

.. caution::
    Do not use a Django version below 1.7! It will not work.

.. tip::
    If you have installed pip you can just use ``pip install -r requirements.txt``


Setting up the demo
===================

    1. Download the source
    2. Extract to a folder of your choice
    3. Open console and change to that folder
    4. Type ``python manage.py creadeb``
    5. Create an superuser when you're asked
    6. Type ``python manage.py runserver``
    7. Open your browser and go to http://127.0.0.1:8000
    8. Login with the username and password you created at step #4

.. hint::
    You can use the superuser to browse the CMS backend at http://127.0.0.1:8000/admin/

.. note::
    If you're using an non-admin user you should assign permissions


Setting up for development
==========================

You first need to install some more packages

    Optional dev apps:
        - django-debug-toolbar
        - django-extensions
        - django-compressor

    For documentation:
        - Sphinx
        - sphinx-rtd-theme

.. tip::
    If you have installed pip you can just use ``pip install -r dev-requirements.txt``


    GIT clone from::
        https://github.com/tfroehlich82/koalixcrm.git
