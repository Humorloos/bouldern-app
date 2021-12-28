"""This file contains models for the accounts app"""
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField


class User(AbstractUser):
    """Custom user class with identifying email field"""
    username = CharField(max_length=30, unique=False)
    email = EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
