"""This file contains custom model manager classes"""
from django.contrib.auth.models import UserManager


class OnlyActiveUserManager(UserManager):
    """
    UserManager that only returns active user instances. It is used for
    re-activating users when registering with an email-address of a deleted
    user.
    """
    def get_queryset(self):
        """
        Gets a queryset with all active users
        :return: a queryset with all active users
        """
        return super().get_queryset().filter(is_active=True)
