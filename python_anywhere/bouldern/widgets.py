from django.forms import TextInput


class CoordinatesWidget(TextInput):
    def format_value(self, value):
        return value.geojson
