# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

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

# import flask app but need to call it "application" for WSGI to work
from flask_app import app as application  # noqa
