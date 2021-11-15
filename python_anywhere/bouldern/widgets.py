"""This module contains custom widgets for bouldern app"""
from django.forms import TextInput


class CoordinatesWidget(TextInput):
    """
    Widget for serializing coordinates into text input fields in geojson format
    """
    def format_value(self, value):
        return value.geojson
