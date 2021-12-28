"""This file contains application configuration for the registration app"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration for registration app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'python_anywhere.accounts'
