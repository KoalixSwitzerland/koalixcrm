.. highlight:: rst

Accounting
============

Accouting Periods
-------------------------

An Accounting Period is the timeframe over which you make your Profit and Loss calculation. Its often called Fiscal Year,
Business Year or Business Quarter. What ever you like.
Accounting Periods have nothing to do with the Accounts but with the Bookings. When you open an existing Accounting Period you find a list of all Bookings during the period below
as an inline table on the page. Feel free to add your bookings here. Be careful when you set up a new Accounting Period -  koalixcrm does not check if you create bookings that are outside the 
possible Accounting Period range nor does it check if there are two accounting periods for the same time period. It is up to the user to check that.


Account section
---------------

Is a Customer Payment Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are the accounts you are able to select when you choose "register payment" in your invoice detail view as destinations for Customers to pay in to

Is the Open Liabilities Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is not implemented yet because the link between Accounting and CRM is not yet finised for the purchase order side
(where you were buying not selling).
This is usually not used by companies because its to much effort to copy all the invoices they receive from suppliers into
your system. Normally you will only book this manually and store the invoce you got from your supplier physically in a filer
in your office. If you do so think about using a good description so that you find the invoice in case of a tax audit
(I have never had a tax audit in my company but I think they are really interested in such things :-) ).

Is the Open Intrest Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There should only be one Open Intrest Account in your Accounting and it is used to book invoiced contract amounts. You
will have to set this open intrest account. If this is not set on at least one account
the link between Accounting and CRM will not work correctly.

Is a Product Inventory Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may choose this option but it has no effect yet because Product inventory is not yet implemented.


Bookings
--------

A booking is a common part of all accounting. Link to wikipage.

Product Categories
------------------

Product Categories are needed for the interface between the CRM and Accounting. You can introduce different product Categories
for different kinds of companies. In this example, we have an "IT support company". An IT Support company usually provides Support and Hardware. Support can be for on-site support or in-house support. Its possible that the 
support must be bought from an other company because you were not able to do everything yourself. Then the Hardware, you normaly don't produce hardware on your own, you buy them from a supplier.

Now lets record that as the following products you may offer to your customers.

+-------------+---------------------+
| Product Nr. |  Description        |
+-------------+---------------------+
| 1           |  in-house work      |
| 2           |  on-site work       |
| 3           |  computer hardware  |
| 4           |  voip hardware      |
+-------------+---------------------+

To be able to do automatic accounting you will have to set the accounts where you want to book your income and spending for each product.

+------------+------------------+------------------------------------+
|Product Nr. | Earnings Acc.    | Spendings Acc.                     |
+------------+------------------+------------------------------------+
|1.          | Income Support   | Spending Support from third        |
|2.          | Income Support   | Spending Support from third        |
|3.          | Income Hardware  | Spendings Hardware                 |
|4.          | Income Hardware  | Spendings Hardware                 |
+------------+------------------+------------------------------------+

Of course, there are more than four products in your inventary - I hope - and depending on your "love of details" you will
have hundreds of them. Instead of setting the Ernings and Spendings Accounts for every Prdoduct individualy koalixcrm has
useful product categories where you only have to set it once. After that you are able to 
link the product categories when you add a product in your CRM. Its also possible to leave this blank if you dont want to make the link between CRM and Accounting
