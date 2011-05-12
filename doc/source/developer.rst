.. highlight:: rst

koalixcrm For Translators and Modders
=====================================

With this part ot the documentation i address two major groups of developers. First there are the translator - which are not really developer but are a very urgent part of every open source program.
With the second group of developer i mean the real python / django / js Developer.

Translators
-----------

The Application it self
^^^^^^^^^^^^^^^^^^^^^^^
To translate the aplication itself the only thing you have to do is to install the koalixcrm on a linux or windows Machine. Please excuse that i cant give you good advice in how to install
the software under windows i simply have not the nerves to play arround with the windows powershell or the cmd :-).  

cd /var/www/koalixcrm/crm
django-admin makemessages -l yourlanguage
this creates a new directory in this folder called /var/www/koalixcrm/crm/locale/yourlanguage/LC_MESSAGES/
in this directory you find one file called django.po
edit this file in the following way:

Lets say you want to translate koalixcrm to french you will do something like that:
find all msgid's look at the english text.
the next following msgstr will be the place you write your translation.

Example:
msgid "phonenumber"
msgstr "phonenumber"

Adjust it to the following:
msgid "phonenumber"
msgstr "nombre de telefon"

After you finised translating the whole file test your translation by compiling it. 

django-admin compilemessages 

After this you ware able to use your translation. Sometimes its needed to set your language in the /var/www/koalixcrm/settings.py
Go on with your translation for accounting and for djangouserextention folder.
As soon as you finished this part you will be able to work with koalixcrm in your own language. But there is still something missing the templatefiles for pdf creation have to be translated as well.

The templatefiles for PDF creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To translate the templatefiles for PDF creation you will have to adjust the templatefiles in the /var/www/koalixcrm/templatefiles folder. There you find a folder for every language code that was already 
translated by the koalixcrm comunity or me. To add your own language type the following:
cp -R en yourlanguage
now open yourlanguage folder and adjust the content of every xml file.


Modders
------- 

There is currently no API available ... Im going to start with that as soon as possible but certainly after i finished the rest of the user documentation.
