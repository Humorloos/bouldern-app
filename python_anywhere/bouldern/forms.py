"""This module contains forms for the bouldern app"""
from colorfield.widgets import ColorWidget
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet

from .models import Boulder, Color
from .widgets import CoordinatesWidget


class ColorForm(ModelForm):
    """Form for adding new colors"""

    class Meta:
        model = Color
        fields = ['name', 'color']
        widgets = {'color': ColorWidget}


class BoulderForm(ModelForm):
    """Form that contains all data related to single boulders in a gym"""

    def __init__(self, gym, **kwargs):
        super().__init__(initial={'gym': gym}, **kwargs)
        self.fields['gym'].disabled = True

    class Meta:
        model = Boulder
        fields = ['coordinates', 'gym']
        widgets = {
            'coordinates': CoordinatesWidget,
        }


class BaseGymMapFormSet(BaseModelFormSet):
    """Base class for the set of boulder forms in a gym"""

    def __init__(self, **kwargs):
        super().__init__(prefix='boulder', **kwargs)


GymMapFormSet = modelformset_factory(model=Boulder, form=BoulderForm,
                                     formset=BaseGymMapFormSet, extra=0)
