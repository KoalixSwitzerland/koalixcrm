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
The dashboard it the place you start after the loggin in. In the dashboard you find a list of all object types
(called objectlist) in three groups (called application) of such objects: crm, accounting and djangoUserExtentions.

.. image:: /images/dashboard.png

Administrator only
^^^^^^^^^^^^^^^^^^
When you are administrator, you can also find an group called auth where you can manage users and groups. During the
installation you are pleased to create a first, administraor user. Every new created user starts with no privileges.
To be able to log in to the koalixcrm the new user must be moderator. When you want to create an accounting-only user
you must select all accounting privileges in the user_modification_view.

.. image:: /images/userprivileges.png

objects_list
------------
From the dashboard your able to select one object type by clicking on the name of it. What you get is a quite detailed list of
objects of this object type. The objects list is the place you will mostly be in. You have the possibility to select any 
of the listet objects and apply "actions" on it, you can simply press on the id of the object to get a modifie view of the
object.

Adding A New Object To The List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To add a new object to the list you simply have to press the Add button on the top right of the page

.. image:: /images/addbutton.png


Apply An Action On An Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Applying actions on objects is a basic point of using koalixcrm. To be able to remove given objects out of your list you
have to select all objects you want to remove by clicking on the checkbox on the left side of the object list. When you
finished your selection you will see a new selectionfield rising from the bottom of your page. Here you can select what
action you want to apply on ths objects. Serveral things can be done with this actions.

.. image:: /images/checkboxobjectlist.png

.. image:: /images/actionslist.png

Aplly A Filter On The List Of Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
On some list of objects your may apply filter functions. This filter functions can be found on the right side of the page.
Depending on the filter you apply on the list you get a smaller amount of objects

.. image:: /images/filter.png

Do A Search Through All Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The more objects you registered in your system, the more difficult it gets to find the one you are looking for.
On some object lists you will find a search box. The keywords you enter in this searbox will be searched in the objects
name, id, description and so on. All objects that include your selected keywords will be displaieed in the list.

..image:: /images/searchbox.png

object_modify_view
------------------
Lets say you logged into the system as a moderator with enough privileges to modify a customer. You first access the
customer objects list. You will find your 