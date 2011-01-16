.. highlight:: rst

Intro
=====

The Intro should give you a first overview over koalixcrm's basic functions and structure.

Basic Structure
---------------
koalixcrm tries to keep near the real world objects. Lets say you wanna register a customer in koalixcrm then you find
a customer in your koalixcrm. When you just received a question for an quote, you find a quote in your koalixcrm. Same
for many kind of business objects you know in your company.
Every such real world objects is represented in the admin start page (called "dashboard") as row of the applicationtable, every 
objects has a name - of cause - an add and a modifie button. When you want to create a customer you just press the "add"
button in the customer row and you will soon get a form (called "object_modify_view") to fill out save your customer. By pressing the modify-, or the name
button of the object you get a list of all objects (called "objects_list") you already saved.

dashboard
---------
The dashboard it the place you start after the loggin in. In the dashboard you find a list of all objects
(called objectlist) in three groups (called application) of such objects: crm, accounting and djangoUserExtentions.

.. image:: /images/applicationlist.png

Administrator only
^^^^^^^^^^^^^^^^^^
When you are administrator, you can also find an group called auth where you can manage users and groups. During the
installation you are pleased to create a first, administraor user. Every new created user starts with no privileges.
To be able to log in to the koalixcrm the new user must be moderator. When you want to create an accounting-only user
you must select all accounting privileges in the user_modification_view.

.. image:: /images/userprivileges.png


object_modify_view
------------------

objects_list
------------