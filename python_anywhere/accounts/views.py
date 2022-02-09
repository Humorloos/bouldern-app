"""This file contains views for the accounts app"""

# accounts/views.py
from rest_framework.mixins import UpdateModelMixin

from python_anywhere.accounts.models import User
from python_anywhere.accounts.serializers import UserSerializer
from python_anywhere.views import ReversibleViewSet


class UserAPI(ReversibleViewSet, UpdateModelMixin):
    """Rest API for deleting users"""
    basename = 'user'
    queryset = User.objects.all()
    serializer_class = UserSerializer
