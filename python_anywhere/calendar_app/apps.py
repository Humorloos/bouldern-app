"""This file contains application configuration for the bouldern app"""
from django.apps import AppConfig


class CalendarappConfig(AppConfig):
    """
    Configuration for calendar app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calendar_app'
