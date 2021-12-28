"""This module contains forms for the bouldern app"""

from django.contrib.auth.forms import UserCreationForm, UsernameField

from python_anywhere.accounts.models import User


class EmailUserCreationForm(UserCreationForm):
    """Form for adding a new user"""
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}
