"""This module contains forms for the bouldern app"""
from django.forms import ModelForm, BaseFormSet, \
    modelformset_factory

from .models import Boulder
from .widgets import CoordinatesWidget


# Todo: replace with modelform_factory() (https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#modelform-factory-function)
class BoulderForm(ModelForm):
    """Form that contains all data related to single boulders in a gym"""

    class Meta:
        """Configures the Boulder model for this form"""
        model = Boulder
        fields = ['coordinates']
        widgets = {
            'coordinates': CoordinatesWidget,
        }


class BaseGymMapFormSet(BaseFormSet):
    """Base class for the set of boulder forms in a gym"""

    def __init__(self, **kwargs):
        super().__init__(prefix='boulder', **kwargs)


GymMapFormSet = modelformset_factory(Boulder, BoulderForm, extra=0)
