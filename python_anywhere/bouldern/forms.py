"""This module contains forms for the bouldern app"""
from django.forms import ModelForm, formset_factory, TextInput, BaseFormSet

from .models import Boulder


class BoulderForm(ModelForm):
    """Form that contains all data related to single boulders in a gym"""
    class Meta:
        """Configures the Boulder model for this form"""
        model = Boulder
        fields = ['coordinates']
        widgets = {
            'coordinates': TextInput,
        }


class BaseGymMapFormSet(BaseFormSet):
    """Base class for the set of boulder forms in a gym"""
    def __init__(self, **kwargs):
        super().__init__(prefix='boulder', **kwargs)


GymMapFormSet = formset_factory(BoulderForm, extra=0)
