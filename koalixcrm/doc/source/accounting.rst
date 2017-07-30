.. highlight:: rst

Accounting
============

Accouting Periods
-------------------------

An Accounting Period is a Timeframe in which you make your ProfitLoss Calculation. Its often called Fiscal Year or Quarter or Busniess Year. What ever you like.
Accounting Periods have nothing to do with the Accounts but with the Bookings. When you open an existing Accounting Period you find a list of all Bookings during this Accounting below
as inline table on the formular. Feel free to add here your bookings. Be carefull when you set up a new Accounting Period. koalixcrm does not check if you do bookings that are outside the 
possible Accounting Period range nor does it check if there were two accounting periods for the same time set. This is up to the user to check that.


Account
-------

Is a Customer Payment Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These were the possible customer payment accounts you ware able to select when you choose "register payment" in your invoice detail view

Is the Open Liabilities Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is not implemented yet because the link between Accounting and CRM is not yet finised for the purchase order site (where you were buying not selling)
This is anyway most often not used by companies because its to much effort to copy all the invoices you get from your suppliers into your system. Normaly you will only book this manualy and
store the invoce you got form your supplier phsyicaly in a filer in your office. If you do so think about using a good description so that you find the invoice in case of a tax control (in fact 
i never had a tax control in my company but i think they are really intrested in such things :-) )

Is the Open Intrest Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is only one open intrest Account in your Accounting and its used to book invoiced contract amounts. You will have to set this open intrest account. If this si not set on at least one account
the link between Accounting and CRM will now work correctly

Is a Product Inventory Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may already choose this option but it has no effect yet because Product inventory is not yet implemented.


Bookings
--------

A booking is a common part of every accounting. Link to wikipage.

Product Categories
------------------

Product Categories are needed for the Interface between the CRM and the Accounting. You can introduce different product Categories for different kind of companies. When i should make an example to 
explain i make this with a "it support company". A IT Support company usualy provides Support and Hardware. Support can be for on-site support or in-house support. Its possible that the 
support must be bought from an other company because you were not able to do everything yourself. Then the Hardware, you normaly dont produce hardware on your own, you buy them from a supplier.
Now lets fix that to the following products you may offer to your customers.

+-------------+---------------------+
| Product Nr. |  Description        |
+-------------+---------------------+
| 1           |  in-house work      |
| 2           |  on-site work       |
| 3           |  computer hardware  |
| 4           |  voip hardware      |
+-------------+---------------------+

To be able to do automatic accounting you will have to set the accounts where you want to book your income and our spendings for each product.

+------------+------------------+------------------------------------+
|Product Nr. | Earnings Acc.    | Spendings Acc.                     |
+------------+------------------+------------------------------------+
|1.          | Income Support   | Spending Support from third        |
|2.          | Income Support   | Spending Support from third        |
|3.          | Income Hardware  | Spendings Hardware                 |
|4.          | Income Hardware  | Spendings Hardware                 |
+------------+------------------+------------------------------------+

Now there are of cause more than four products in your inventary i hope and depending on your "love on details" you will have hundreds of them. Insted of setting the these
Ernings and Spendings Accounts for every Prdoduct individualy koalixcrm has this useful product categories where you have to set it only once. After that you are able to 
link the product categories when you add a product in your crm. Its also possible to leave this blank if you dont like to make the link between CRM and Accounting