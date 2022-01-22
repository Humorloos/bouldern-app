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

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from googleCalendarApp.constants import CALENDAR_URI
from python_anywhere.bouldern.views import index
from python_anywhere.settings import USER_HOME, MEDIA_URL, MEDIA_ROOT, \
    BOULDERN_URL_SEGMENT, DEVELOPMENT

sys.path = list({str(USER_HOME / project_name) for project_name in
                 ['googleCalendarApp', 'GoogleApiHelper'] + sys.path})

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{BOULDERN_URL_SEGMENT}/', include('python_anywhere.bouldern.urls')),
    path(f'{CALENDAR_URI}/', include('python_anywhere.calendar_app.urls')),
    re_path(r'^favicon\.ico$',
            RedirectView.as_view(url='/static/vue/favicon.ico')),
    # Override email confirmation URL to redirect to frontend view
    re_path(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$',
            index, name='index'),
    path('registration/', include('python_anywhere.accounts.urls')),
    path('registration/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls'))
]

if DEVELOPMENT:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
else:
    urlpatterns += [path('', index, name='index')]
    # History API Fallback
    urlpatterns += [re_path(r'^.*', index, name='index')]
