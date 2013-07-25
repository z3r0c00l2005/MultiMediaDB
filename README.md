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
6. Install Python Imaging Library 1.1.7
7. Install ReportLAB 2.7
8. Install setuptools 0.9.8
9. Install Geraldo 0.4.17
10. Install apache 2.4.4
11. Add the folowing to the system path environment variable - ;c:\python27;c:\Program Files\MySQL\MySQL Server 5.6\bin
12. Extract and install the Django framework by issuing the command "python setup.py install" within the folder
13. Copy the mod_wsgi.so file to "C:\Program Files\Apache Software Foundation\Apache2.4\modules"
14. Copy the httpd.conf file to "C:\Program Files\Apache Software Foundation\Apache2.4\conf" (Overwrite the existing one)
15. Create the MySQL database
15.a. login to MySQL - mysql -uthssdb -pthssdb
15.b. Create database - create database thssmultimedia;
16. Copy the "MultimediaDB" folder to c:\
17. Create the default database schema
17.a. Navigate to c:\MultimediaDB
17.b Run "python manage.py syncdb"
17.c. Type "no" when asked to create a user
18. Restart Apache and test!

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

