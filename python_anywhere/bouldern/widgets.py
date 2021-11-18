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
    option_template_name = 'bouldern/difficulty_level_select_option.html'

    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0/jquery.min.js',
            'bouldern/js/difficulty_level_widget.js')
