.. highlight:: rst

Django User Extention
=====================

Introduction
------------

The django Framework supports some basic users, authentification and groups permissions. This is ok for most of all
django apps. In the koalixcrm there are some additional information for users needed. To be able to generate PDF's
we need some information about the user that is generating the documents. There are some obvious fields like the 
internal phone address that is printed on every documnet - if you like. But there are also some "behind the scene" fileds
needed. In this chapter i describe all of them in a bit more detail view.

If you are administrator of this koalicrm instance: Its recommended that you give add/modifiy access to this userextentions
only to either youself and/or your boss. Users of koalixcrm really dont need to get access to this part of koalicrm

FOP PDF Creation
^^^^^^^^^^^^^^^^

Befor i start describing how you can set up the User Extention this short section will explain you a bit what is going on when you create pdfs.

In koalixcrm you are able to set up and store contract with invoices, quotes and so on. This is quite cool but worthless when you have no ability to 
print this things for your customers. This is the point where it starts to get difficult in django ... and of cause also in most other framworks, the
export of data is a little bit difficult. For django most people pefer using ReportLab but not koalixcrm: Out of the following reasons:
 - The input files are not in a common format.
 - Does not seem to be very open ... and i dont like that.
 - It doesnt seem its built for letter creations
Now all these requirements are fully covered by an other pdf creation tool: apache-fop. All would be perfect when this apache-fop wouldnt be programmed in JAVA

Anyway, koalixcrm uses apache-fop to create PDFs for now and its not planned to change this until i run into huge problems.

How does this work:
  1. When you select "create a PDF of your invcoe" in the actions list of your invoice, a XML file of all the django bojects is created in the /tmp folder of your system
  2. Now django executes a os.system command called "fop -c (configurationfile) -xml (the createdxmlfile) -xsl (your xsl file) -pdf (the output pdf file)"
  3. If the command creates any error you will not see it in django!! This is very hard to debug and the reason why koalixcrm writes a /tmp/tmp.log with the command koalixcrm used to create
the pdf. To get the error message follow do exacly this: sudo su www-data; cd; cat /tmp/tmp.log | bash; This will give you a good error message.


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