.. highlight:: rst

************
Installation
************

.. note::
    This version is not recommended for productive use. Therefore productive installation is not yet mentioned in this documentation.

.. contents::


By platform
-----------

Pango, GdkPixbuf, and cairo can not be installed
with pip and need to be installed from your platform’s packages.
lxml and CFFI can, but you’d still need their own dependencies.
This section lists system packages for lxml or CFFI when available,
the dependencies otherwise.
lxml needs *libxml2* and *libxslt*, CFFI needs *libffi*.
On Debian, the package names with development files are
``libxml2-dev``, ``libxslt1-dev`` and ``libffi-dev``.

Debian / Ubuntu
~~~~~~~~~~~~~~~

Debian 7.0 Wheezy or newer, Ubuntu 11.10 Oneiric or newer:

.. code-block:: sh

    sudo apt-get install python-dev python-pip python-lxml libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info


Debian 6.0 Squeeze, Ubuntu 10.04 Lucid:
GDK-PixBuf is part of GTK+, which also depends on cairo and Pango.

.. code-block:: sh

    sudo apt-get install python-dev python-pip python-lxml libgtk2.0-0 libffi-dev

Fedora
~~~~~~

.. code-block:: sh

    sudo yum install python-devel python-pip python-lxml cairo pango gdk-pixbuf2 libffi-devel

Archlinux
~~~~~~~~~

.. code-block:: sh

    sudo pacman -S python-pip python-lxml cairo pango gdk-pixbuf2


Gentoo
~~~~~~

.. code-block:: sh

    emerge weasyprint


Mac OS X
~~~~~~~~

With Macports

.. code-block:: sh

    sudo port install py27-pip py27-lxml cairo pango gdk-pixbuf2 libffi

With Homebrew:

.. code-block:: sh

    brew install python cairo pango gdk-pixbuf libxml2 libxslt libffi


Windows
~~~~~~~

* Get CPython 2.7 `from python.org <http://www.python.org/download/>`_,
* `Christoph Gohlke’s unofficial binaries
  <http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml>`_ for CFFI and lxml,
* and `Alexander Shaduri’s GTK+ installer
  <http://gtk-win.sourceforge.net/home/index.php/Main/Downloads>`_.
  Make sure that *Set up PATH environment variable* checked.


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
    4. Execute ``python manage.py creadeb``
    5. Create an superuser when you're asked for
    6. Execute ``python manage.py runserver``
    7. Open your browser and go to http://127.0.0.1:8000
    8. Login with the username and password you created at step #4

.. hint::
    You can use the superuser to browse the CMS backend at http://127.0.0.1:8000/admin/

.. note::
    If you're using an non-admin user you should assign permissions


Install the initial data
========================

To install the initial user groups do the following:

    1. Open console and change to project folder
    2. Execute ``python manage.py loaddata auth_groups``


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


    GIT clone from:
        https://github.com/tfroehlich82/koalixcrm.git
