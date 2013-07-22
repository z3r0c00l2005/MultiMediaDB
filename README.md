MultiMediaDB
============

Django version of THSS MM DB


Install
-------
1. Microsoft .Net Framework 4
2. Microsoft Visual C++ 2010 redist
3. Install MySQL 5.6.11
3.a. Configure as a "Server" machine
3.b. Create a user with DBA privileges - Username: thssdb Password: thssdb
4. Install Python 2.7.5 for all users
5. Install mysql-python 
6. Install apache 2.4.4
7. Add the folowing to the system path environment variable - ;c:\python27;c:\Program Files\MySQL\MySQL Server 5.6\bin
8. Extract and install the Django framework by issuing the command "python setup.py install" within the folder
9. Copy the mod_wsgi.so file to "C:\Program Files\Apache Software Foundation\Apache2.4\modules"
10. Copy the httpd.conf file to "C:\Program Files\Apache Software Foundation\Apache2.4\conf" (Overwrite the existing one)
11. Create the MySQL database
11.a. login to MySQL - mysql -uthssdb -pthssdb
11.b. Create database - create database thssmultimedia;
12. Copy the "MultimediaDB" folder to c:\
13. Create the default database schema
13.a. Navigate to c:\MultimediaDB
13.b Run "python manage.py syncdb"
13.c. Type "no" when asked to create a user
14. Restart Apache and test!

Troubleshooting
---------------
Check paths in c:/MultimediaDB/thssdb/django.wsgi
Check paths in C:\Program Files\Apache Software Foundation\Apache2.4\conf\httpd.conf

Notes
-----
The version of mod_wsgi is dependent on the architecture and version of Apache used.
The version of MySQL-python is dependent on the version of python used.
Django 1.5.1 needs python 2.7.
Source is stored under git version control - https://github.com/z3r0c00l2005/MultiMediaDB

