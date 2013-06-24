import os, sys
sys.path.append('C:/Program Files/Apache Software Foundation/Apache2.4/htdocs/thssdjango')
sys.path.append('C:/Program Files/Apache Software Foundation/Apache2.4/htdocs/thssdjango/thssdb')
sys.path.append('C:/Program Files/Apache Software Foundation/Apache2.4/htdocs/thssdjango/multimediadb')
sys.path.append('C:/Program Files/Apache Software Foundation/Apache2.4/htdocs/thssdjango/filetransfers')
os.environ['DJANGO_SETTINGS_MODULE'] = 'thssdb.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
