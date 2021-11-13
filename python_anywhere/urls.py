"""python_anywhere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from googleCalendarApp.constants import CALENDAR_URI
from python_anywhere.bouldern.constants import BOULDERN_URI
from python_anywhere.settings import USER_HOME

sys.path = list({str(USER_HOME / project_name) for project_name in
                 ['googleCalendarApp', 'GoogleApiHelper'] + sys.path})

urlpatterns = \
    [path(f'{BOULDERN_URI}/', include('python_anywhere.bouldern.urls')),
     path(f'{CALENDAR_URI}/', include('python_anywhere.calendar_app.urls')),
     path('admin/', admin.site.urls),
     url(r'^favicon\.ico$',
         RedirectView.as_view(url='/static/images/favicon.ico')), ]
