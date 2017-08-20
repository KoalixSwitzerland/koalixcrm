.. highlight:: rst

Intro
=====

This Intro should give you an overview of koalixcrm's basic functions and structure.

Basic Structure
---------------
koalixcrm tries to keep its structure near the real world objects it represents. Lets say you want to register a customer in koalixcrm then you find
a customer in your koalixcrm. When you receive a question for a quote, you find the quote in your koalixcrm. Same
for many kind of business objects you know in your company.
Every such real world objects is represented in the admin start page (called "dashboard") as row of the Applications table. Every object has a name - of cause - an Add and a Change button. When you want to create a customer you just press the "Add"
button in the Customers row and you will see a form (called "object_modify_view") to fill out for your customer. By pressing
the Change or name button (eg "Customers") of the object you see a list of all objects (called "objects_list") you have
already saved.

dashboard
---------
The dashboard ("Site Administration") is the place you start after logging in. In the dashboard you find a list of all object types
(called objectlist) in three groups (called applications): crm, accounting and djangoUserExtentions.

.. image:: /images/dashboard.png

Administrator only
^^^^^^^^^^^^^^^^^^
When you are administrator, you can also see a group called auth where you can manage users and groups. During the
installation you are asked to create a first, administrator user. Every new user after that starts with no privileges.
To be able to log in to koalixcrm the new user must be moderator. When you want to create an accounting-only user
you must select all accounting privileges in the user_modification_view.

.. image:: /images/userprivileges.png

objects_list
------------
From the dashboard you are able to select one object type by clicking on the name of it. What you get is a quite detailed list
of objects of this object type. The objects list is the place you will be in most. You have the possibility to select any 
of the listed objects and apply "actions" to them, you can simply press on the id of the object to get a modifiable view of
the object.

Adding A New Object To The List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To add a new object to the list you simply have to press the Add button on the top right of the page

.. image:: /images/addbutton.png


Apply An Action On An Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Applying actions to objects is a basic point of using koalixcrm. To be able to remove objects from your list you
have to select all objects you want to remove by clicking on the checkbox on the left side of the object list. When you
finish making your selection you will see a new selection field rising from the bottom of your page. Here you can select
what action you would like to to apply to the objects. Serveral things can be done with these actions.

.. image:: /images/checkboxobjectlist.png

.. image:: /images/actionslist.png

Apply A Filter On The List Of Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
On some list of objects you may apply filter functions. This filter function can be found on the right side of the page.
Depending on the filter you apply on the list you get a smaller number of objects

.. image:: /images/filter.png

Do A Search Through All Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The more objects you registered in your system, the more difficult it becomes to find the one you are looking for.
On some object lists you will find a search box. The keywords you enter in this searbox will be searched in the objects
name, id, description and so on. All objects that include your selected keywords will be displayed in the list.

..image:: /images/searchbox.png

object_modify_view
------------------
Lets say you logged into the system as a moderator with enough privileges to modify a customer. You first access the
customer objects list. You will find your 
