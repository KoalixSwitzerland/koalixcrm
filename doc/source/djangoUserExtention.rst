.. highlight:: rst

Django User Extention
=====================

Introduction
------------

The django Framework supports some basic users, authentification and groups permissions. This is ok for most of all
django apps. In the koalixcrm there are some additional information for users needed. To be able to generate PDF's
we need some information about the user that is generating the documents. There are some obvious fields like the 
internal phone address that is displyed on every documnet - if you like. But there are also some "behind the scene" fileds
needed. In this chapter i describe all of the in a bit more detail view.

If you are administrator of this koalicrm instance: Its recommended that you give add/modifiy access to this userextentions
only to either youself and/or your boss. Users of koalixcrm really dont need to get access to this part of koalicrm

Objecttypes
-----------

User Extentions
^^^^^^^^^^^^^^^
The Users

..image::

XSL Files
^^^^^^^^^

TemplateSet
^^^^^^^^^^^
A TemplateSet is a set of xsl-templatefiles, Header and Footer Texts. A first Templateset is installated by the command
./manage koalixcrm_install_defaulttemplates but you can also define and install your own xsl files by setting up your own 
templateset and selecting it in the user Extention of your own user.