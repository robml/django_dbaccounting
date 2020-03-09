# django_dbaccounting
 A Python based accounting core built with Django

DB Accounting
==============

DB Accounting is a Django app that provides a core for accounting and account management.
Although developed primarily for accounting purposes, the flexible nature of DB Accounting,
allows it to be configured for anything that represents the need for categories, accounts, and transactions.

Detailed documentation is in the "docs" directory.

Quick start
-----------

If you are only looking to install the python package, use:
- pip install db-accounting
- download the .tar file from Github
- install it from DjangoPackages.org

To configure:

1. Add "dbaccounting" to your INSTALLED_APPS setting like this::
	
	INSTALLED_APPS  [
		...
		'dbaccounting',
	]

2. Include the dbaccounting URLconf in your project urls.py like this::
	
	path('fin/',include('dbaccounting.urls')),

3. Run ``python manage.py migrate`` to create the dbaccounting models.

4. Start the development server and visit http://127.0.0.1:8000/admin
   to create Account Types and Accounts (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/fin/ to manage your accounts.

-----
Notes
-----
This is the first version so far, and some of the side links are not properly configured yet
(e.g. Balance Sheet rendering, etc). The application thus far provides core functionality for
transactions in general , which will be extended in future versions.

Special thanks to those using this package and the feedback given. What started out as a side project
to help a few startups has now increased to include the open-source community. The package is coupled with
over 100 tests just to test the core functionality itself, and I have done my best to optimize for performance
and memory.

If you liked this package, leave a star, and feel free to join my mailing list on robmel.com, where I occasionally
send out insights and goodies from tech, finance, AI and link them to the individual level.

Best,
Robert M.

Reach me on instagram: @officialrobmel or @quantrobbie

See my Github: @robml
