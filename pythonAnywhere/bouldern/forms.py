from django import forms
from django.contrib.gis.forms import PointField

from widgets import GymMapWidget


class GymMapForm(forms.Form):
    gym_map = PointField(label='Gym Map', widget=GymMapWidget(
        attrs={'map_width': 800, 'map_height': 500}))
