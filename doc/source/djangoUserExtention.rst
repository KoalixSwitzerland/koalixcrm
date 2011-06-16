.. highlight:: rst

Django User Extension
=====================

Introduction
------------

The Django Framework supports some basic users, authentication and groups permissions. This is OK for most of all
Django apps. In the koalixcrm there are some additional information for users needed. To be able to generate PDF's
we need some information about the user that is generating the documents. There are some obvious fields like the 
internal phone address that is printed on every document - if you like. But there are also some "behind the scene" fields
needed. In this chapter i describe all of them in a bit more detail view.

If you are administrator of this koalixcrm instance: Its recommended that you give add/modify access to this user-extension
only to either yourself and/or your boss. Users of koalixcrm really don't need to get access to this part of koalixcrm

FOP PDF Creation
^^^^^^^^^^^^^^^^

Before i start describing how you can set up the User Extension this short section will explain you a bit what is going on when you create PDF's.

In koalixcrm you are able to set up and store contract with invoices, quotes and so on. This is quite cool but worthless when you have no ability to 
print this things for your customers. This is the point where it starts to get difficult in Django ... and of cause also in most other frameworks, the
export of data is a little bit difficult. For Django most people prefer using ReportLab but not koalixcrm: Out of the following reasons:

 - The input files are not in a common format.
 - Does not seem to be very open ... and i don't like that.
 - It doesn't seem its built for letter creations

Now all these requirements are fully covered by an other PDF creation tool: apache-fop. All would be perfect when this apache-fop wouldn't be programmed in JAVA

Anyway, koalixcrm uses apache-fop to create PDF's for now and its not planned to change this until i run into huge problems.

How does this work:

  1. When you select "create a PDF of your invoice" in the actions list of your invoice, a XML file of all the Django objects is created in the /tmp folder of your system
  2. Now Django executes a os.system command called "fop -c (configurationfile) -xml (the createdxmlfile) -xsl (your xsl file) -pdf (the output pdf file)"
  3. If the command creates any error you will not see it in Django!! This is very hard to debug and the reason why koalixcrm writes a /tmp/tmp.log with the command koalixcrm used to create
     the PDF. To get the error message follow do exactly this: sudo su www-data; cd; cat /tmp/tmp.log | bash; This will give you a good error message.

As you can see there are several files needed to get from a xml to a pdf. These files can be stored in the TemplateSet of the UserExtension-Part of koalixcrm. You can define as many different TemplateSets
you like. This makes sens because sometimes you want different users having different pdf styles or you want to be able to access an old style because a new one has an bug.

Object types
------------

User Extensions
^^^^^^^^^^^^^^^

The Users Extension is a container for all kind of Infromation that is needed to create a PDF with user specific information in it.


XSL Files
^^^^^^^^^


TemplateSet
^^^^^^^^^^^

As described in the first part of this chapter the templateset is the place where you compose a templete style set for users. This Templatesets were refered in the UserExtension and must be
set in order to be able to create PDFs. A TemplateSet constists of folliwing parts:

- Invoice XSL File
- Quote XSL File
- Purchase Order XSL File
- Purchase Confirmation XSL File
- Deilvery Order XSL File


A TemplateSet is a set of xsl-templatefiles, Header and Footer Texts. A first Templateset is installed by the command
./manage koalixcrm_install_defaulttemplates but you can also define and install your own xsl files by setting up your own 
templateset and selecting it in the user Extension of your own user.