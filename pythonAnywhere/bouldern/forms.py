from django.contrib.gis.forms import PointField
from django.forms import Form

from .widgets import GymMapWidget


class GymMapForm(Form):

    def __init__(self, gym, **kwargs):
        super().__init__(**kwargs)
        self.fields['gym_map'] = PointField(
            label='Gym Map',
            widget=GymMapWidget(attrs={
                'map_width': 800, 'map_height': 500, 'gym': gym}))
