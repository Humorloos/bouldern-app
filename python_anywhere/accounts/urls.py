"""URL mappings for accounts app"""

# accounts/urls.py
from django.urls import re_path
from rest_framework.routers import SimpleRouter

from python_anywhere.accounts.views import UserAPI
from python_anywhere.bouldern.views import index

router = SimpleRouter()
router.register(UserAPI.basename, UserAPI)
urlpatterns = router.urls + [
    re_path(r'^password/reset/change/(?P<uidb64>[0-9A-Za-z_\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
            index, name='password_reset_confirm'),
    # Override email confirmation URL to redirect to frontend view
    re_path(r'^account-confirm-email/.*/$', index, name='index'),
]
