"""URL mappings for registration app"""

# registration/urls.py
from django.urls import path

from python_anywhere.accounts.views import SignUpView, UserDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('quit/', UserDeleteView.as_view(), name='quit'),
]
