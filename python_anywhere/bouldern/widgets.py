"""This module contains custom widgets for bouldern app"""
from django.forms import TextInput, Select


class CoordinatesWidget(TextInput):
    """
    Widget for serializing coordinates into text input fields in geojson format
    """

    def format_value(self, value):
        return value.geojson


class DifficultyLevelWidget(Select):
    """
    Widget for choosing a difficulty level from a dropdown showing the level's
    colors
    """
    template_name = 'bouldern/difficulty_level_select.html'
    option_template_name = 'bouldern/difficulty_level_select_option.html'
