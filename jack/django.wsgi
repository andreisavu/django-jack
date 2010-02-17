
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'jack.settings'

import django.core.handlers.wsgi

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

application = django.core.handlers.wsgi.WSGIHandler()

