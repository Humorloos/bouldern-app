"""This file contains models for the accounts app"""
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import EmailField, CharField

from python_anywhere.accounts.managers import OnlyActiveUserManager


class User(AbstractUser):
    """Custom user class with identifying email field"""
    objects = OnlyActiveUserManager()
    all_objects = UserManager()

    username = CharField(max_length=30, unique=False)
    email = EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
