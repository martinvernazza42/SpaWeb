import sys
import os

project_home = '/home/martinvz/SpaWeb'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'spa.configuraciones.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
