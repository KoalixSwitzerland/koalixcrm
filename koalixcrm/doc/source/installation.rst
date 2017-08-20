.. highlight:: rst

Installation
============

External requirements
^^^^^^^^^^^^^^^^^^^^^

koalixcrm requires Apache Fop to print its documents. Macports, Debian
derivatives and likely others have 'fop' packages which can be installed.

Be aware that ``/usr/bin/fop`` is hard coded in multiple places throughout
koalixcrm and if your install of Fop is elseware you will need to symlink it in
to place.


koalixcrm
^^^^^^^^^

koalixcrm's Python requirements are installed by setup.py, so if you are
installing via that mechanism all that is required is::

  python setup.py

from the koalixcrm source root.


Manual install
==============

If you are performing a manual install, the depenencies can be installed with::

  pip install -r requirements.txt

From the base of the koalixcrm source tree. Note that these may be out of sync
with those specified in setup.py and it is good to check before installing
them.

