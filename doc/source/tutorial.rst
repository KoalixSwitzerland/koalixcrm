.. highlight:: rst

Tutorial
========

Befor your start I recommend you first have a look into the :doc:`intro`. This gives you a first idea of the basic structure 
of the koalixcrm. When you understand the structure and functions of koalixcrm or any other large django application 
you are ready to start with the tutorial. I recommend further that you have firefox installed, and did have a look
at the :doc:`installation` - and installed the koalixcrm according to this description on your apache2 webserver.

Create Your First Customer
--------------------------
Let say you want to Register the following Customer:
Privat address:

John Smith
Ave 1
90990 Smallville
Phone: 
Mobile:
Email:

Business address:
Smith and Sons
Ave 2
120987 Largeville
Phone: 
Mobile:
Email:

Logging In Adminpage
^^^^^^^^^^^^^^^^^^^^
Depending on where you installed your koalixcrm - in our tutorial i expect you installed it on your localhost (the
computer your sitting in front of) - Visit the http://localhost/admin page in your browser. Please use Firefox for this 
first test, it seems as if there exist the less bugs in grappelli with this browser. 
You will soon find the login page

..image:: /images/adminlogin.png

fill out the username and password you set in the :doc:`installation` in the syncdb procedure.

Select "Add Customer"
^^^^^^^^^^^^^^^^^^^^^
After the login you will find the dashboard you already know from the :doc:`intro`. In the Apllicationlist select the
"Customer" - add button

..image:: /images/customeraddbutton.png

Fill out Fields
^^^^^^^^^^^^^^^
After adding the customer you will have to fill out all required values to get a valid registered customer. Finish the 
customer registration by pressing the save button

..image:: /images/customerdetailedaddingview.png

Look at your first Customer
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ok now we registered your first Customer.
Of cause to have a customer is not that interesting, we hope that a customer is going to order something, or needs an
invoice, a quote or something else. This will e the next step of the tutorial. But furst have a look at your bright shiny
customer by selecting customer's in the dashboard as described in the :doc:`intro`. 

Create Your First Contract
--------------------------
I expect your still looking at your first customer we just created:


Register The Invoice In The Accounting
--------------------------------------

