Description
-----------
The e-xact sample shopping cart (found at http://store.e-xact.com/) implemented starting with a django app.

Requirements
------------
Django version 1.1.1
sqlite3

Setup
-----
1.  Get code.
2.  Load data : python manage.py syncdb
3.  Create your chase paymentech hosted checkout payment page.
4.  On the payment page, ensure your receipt link url points to http://your-domain:[port]/shop/payment_notification and that you have entered text into 'receipt text'.
5.  Configure your settings.py

  * PAYMENT_PAGE_VARS['x_login'] corresponds to 'payment page id' in the paymentech admin

  * PAYMENT_TRANSACTION_KEY corresponds to 'transaction key' in the paymentech admin

  * PAYMENT_PAGE_VARS['x_fp_sequence'] should be a random string

