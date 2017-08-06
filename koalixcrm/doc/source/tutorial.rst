.. highlight:: rst

Tutorial
========

This tutorial is going to teach you how to 
  
  1. Create a customer 
  2. Create a currency
  3. Create a product
  4. Create a contract
  5. Create a quote
  6. Create an invoice
  7. Set up your accounting
  8. Record an invoice in your accounting
  9. Record a customer payment in the accounting

Before you start I recommend you first have a look into the :doc:`intro`. This gives you an idea of the basic structure 
of koalixcrm. When you understand the structure and functions of koalixcrm or any other large Django application 
you are ready to start with the tutorial. Further, I recommend that you have Firefox installed, have a look
at the :doc:`installation` section - and install koalixcrm according to this description on your Apache2 webserver.

Create Your First Customer
--------------------------
Let say you want to Register the following Customer:
Private address::

  John Smith
  Ave 1
  90990 Smallville
  Phone: 
  Mobile:
  Email:

Business address::

  Smith and Sons
  Ave 2
  120987 Largeville
  Phone: 
  Mobile:
  Email:

Logging In Adminpage
^^^^^^^^^^^^^^^^^^^^

Depending on where you installed your koalixcrm - in our tutorial I assume you installed it on your localhost (the
computer you are sitting in front of) - visit http://localhost/admin in your browser. Please use Firefox for this 
first test, it seems as if there are fewer bugs in grappelli with that browser. 
You will soon see the login page

.. image:: /images/adminlogin.png

fill out the username and password you set during :doc:`installation` in the syncdb procedure.

Create a Currency
^^^^^^^^^^^^^^^^^

.. image:: /images/addcurrencyform.png

Select "Add Customer"
^^^^^^^^^^^^^^^^^^^^^

After login you will see the dashboard you already know from the :doc:`intro`. In the Applications list select the
"Customer" - add button

.. image:: /images/customeraddbutton.png

Fill out Fields
^^^^^^^^^^^^^^^

After adding the customer you will have to fill out all required values to get a valid registered customer.
You will have to fill out "postal address" and "phone address". Further you will need to add a new "Default Billing Cycle"
This can be added by pressing the greeen "plus" sign beside the "Default billing cycle" drop down box.
A new page will open up and give you the ability to add a new billing cycle. Fill in the values as described in the image below:

.. image:: /images/addcustomerbillingcycleform.png

After you filled in all required values you will have to click on the save button. This click will bring you back to the customer adding view ... and you will see that the default payment method is now set. Next is the customer group, we
have to do exatly the same. Click on the green "plus" sign beside the groups list and you will soon get a pop up where
you can add your first default customer group. Fill in the values as described in the image below

.. image:: /images/addcustomergroupform.png

After that you have to fill out all the addresses defined in the header of this tutorial.
Finish the customer registration by pressing the save button

..  image:: /images/addcustomerform.png


Look at your first Customer
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ok now we have registered your first Customer.
Of course to have a customer is not that interesting, we hope that a customer is going to order something, or needs an
invoice, a quote or something else. This will be the next step of the tutorial. But first have a look at your bright shiny
customer by selecting customer's id the dashboard as described in the :doc:`intro`. 

Create Your First Contract
--------------------------
I expect you are still looking at your first customer we just created. The next step is to click the checkbox to the left
of your customer on the CRM customer list and look at the the actions list that appears on the bottom of the page.

.. image:: /images/customeractions.png

Select "Create Contract" from this list. This will bring you to the "add contract" form. The advantage of doing it this way
- instead of adding a new contract through the dasboard - is that you have some values, like the default customer, already
set. this will give you some additional seconds for your daily work.
I expect you are a little bit surprised ... where do I select that I want to have a quote or an invoice? Well, in 
koalixcrm a contract is not an invoice and a contract is not a quote. A contract is simply a place to store all kind
of documents that are related to the contract. This can of course be a invoice or a quote but also purchase orders and so on.

Fill in the description field, then by clicking on the save button you have finished the creation of a contract.

Create Your First Quote
-----------------------

Until now there are no products, no prices and no units registed. In order to be able to offer a product to a customer
we need some products first.... you could do it the lazy way by adding the product while registering the 
quote but in this case we are going to register the products, units and prices before we create the quote.

Create Your First Product
^^^^^^^^^^^^^^^^^^^^^^^^^
To create your first product visit the dashboard by either following the breadcrumps back to the dashboard

.. image:: /images/breadcrumps.png

or visit http://localhost/admin again. Press the Add button next to Units to access the Unit adding form. Now fill out all the
required fields to register the unit "hours"

.. image:: /images/addunitformhour.png

Press save, add an other unit by again pressing the add button.
Now we create a unit "minute".

.. image:: /images/addunitformminute.png

Pess save and go back to the dashboard

As we have registered some units, now we are able to create a product.

Press the Products add button to get to the products adding form. We start with a common product called Manpower.
Fill all fields with the following values:

.. image:: /images/addproductform1.png

as you know every product has its price espencialy manpower - time is money. Thats why we have to add at least
one price for this product by giving the Prices fields the following values.

.. image:: /images/addproductform2.png

You will see an other part of this form called Unit Transfroms. Unit Transforms are sometimes needed when, for example, you have
stacks of certain products but only one price per piece. Leave this blank when you only have one unit for one product.

After adding this product you are ready to create your first Quote by going to your dashboard. Open Contracts, select
the check box beside the contract you want to change and select "Create Quote" from the Actions list. A form will open for 
you to fill out your fist quote.

.. image:: /images/addquoteform1.png

As you can see, there are lots of predefined values because we created the quote with the action instead of via dasboard
and Quote Add. There are three major parts of a quote:

 * First the general values like "valid until", "description" and so on
 * Second are role positions of the quote
 * Lastly are Addresses related to the Contract

By pressing the "+" sign you can add as many positions as you like. Fill in the values as described below.

.. image:: /images/addquoteform2.png

Click on the save button to finish your first quote. Go back to the dashboard, go to quotes and select the newly created
quote's checkbox. From the actions select "Create PDF of Quote" to generate a pdf of this new quote.

NOTE! You are currently required to do a recalculation of the prices before you create the pdf. You can do
this by selecting your quote and choose recalculate prices form the actions list.

Create Your First Invoice
-------------------------
This is going to be a very short chapter because all you have to do is repeat the steps above but insted of selecting
"Create Quote" in the Contract Actions list you select "Create Invoice"; alternatively by selecting your new Quote and use the action
"Create Invoice". The second way is much easier and faster because the program just takes all values and positions from the
quote and transforms it into a invoice.


Register The Invoice In Accounting
----------------------------------
To be able to register the invoice in koalixcrm's Accounting we need to set up Accounting and adjust your products. 

Create Accounts
^^^^^^^^^^^^^^^
Currently there is only a Swiss accounts table. I really hope to get some help soon to create some generic account tables for other 
countries because if you have to fill all them out on your own this is going to take quite some time.

Its urgent that you have you have set up at least these special accounts:

1. Open Reliabilities
2. Open Intrests
3. Customer Payment Account



Create Product Accounting Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

