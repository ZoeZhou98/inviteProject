"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import time
import traceback
import signal

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

#application = get_wsgi_application()


 
from os.path import join,dirname,abspath

PROJECT_DIR = dirname(dirname(abspath(__file__)))

sys.path.insert(0,PROJECT_DIR)
 
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
 
#application = get_wsgi_application()
try:
    application = get_wsgi_application()
    print 'WSGI without exception'
except Exception:
    print 'handling WSGI exception'
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
