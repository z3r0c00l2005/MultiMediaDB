import os, sys
sys.path.append('C:/MultimediaDB')
sys.path.append('C:/MultimediaDB/thssdb')
sys.path.append('C:/MultimediaDB/multimediadb')
sys.path.append('C:/MultimediaDB/filetransfers')
os.environ['DJANGO_SETTINGS_MODULE'] = 'thssdb.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
