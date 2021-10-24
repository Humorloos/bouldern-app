# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

# +++++++++++ DJANGO +++++++++++
# To use your own Django app use code like this:
import os
import sys
from pathlib import Path

# add your project directory to the sys.path
user_home = Path('/home/Humorloos')
sys.path = list({path for path in [str(user_home.joinpath(project_name)) for project_name in [
    'googleCalendarApp',
    'GoogleApiHelper',
    'bouldernFormsApp',
    'pythonAnywhere',
    'bouldern'
]] + sys.path})
print(sys.path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
