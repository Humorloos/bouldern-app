"""URL mappings for accounts app"""

# accounts/urls.py
from django.urls import path
from rest_framework.routers import SimpleRouter

from python_anywhere.accounts.views import SignUpView, UserDeleteView, UserAPI

router = SimpleRouter()
router.register(UserAPI.basename, UserAPI)
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('quit/', UserDeleteView.as_view(), name='quit'),
] + router.urls
