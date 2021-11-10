from PIL import Image
from django.contrib.gis.forms import PointField
from django.contrib.staticfiles.finders import find
from django.forms import Form

from .widgets import GymMapWidget


class GymMapForm(Form):

    def __init__(self, gym, **kwargs):
        super().__init__(**kwargs)
        map_width, map_height = Image.open(
            find(f'bouldern/images/{gym}/hallenplan.png')).size
        self.fields['gym_map'] = PointField(
            widget=GymMapWidget(attrs={
                'map_width': map_width, 'map_height': map_height, 'gym': gym,
                'disabled': True}))
