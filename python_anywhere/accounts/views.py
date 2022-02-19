"""This file contains views for the accounts app"""

# accounts/views.py
from rest_framework.mixins import DestroyModelMixin

from python_anywhere.accounts.models import User
from python_anywhere.accounts.serializers import UserSerializer
from python_anywhere.views import ReversibleViewSet


class UserAPI(ReversibleViewSet, DestroyModelMixin):
    """Rest API for deleting users"""
    basename = 'user'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
