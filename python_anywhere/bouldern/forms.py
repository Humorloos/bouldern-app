"""This module contains forms for the bouldern app"""
from colorfield.widgets import ColorWidget
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet, \
    HiddenInput, BaseInlineFormSet
from django.forms import inlineformset_factory

from .models import Boulder, Gym, Color, DifficultyLevel
from .widgets import CoordinatesWidget, DifficultyLevelWidget


class GymForm(ModelForm):
    class Meta:
        model = Gym
        fields = ['name', 'map']


class ColorForm(ModelForm):
    """Form for adding new colors"""

    class Meta:
        model = Color
        fields = ['name', 'color']
        # Todo: check if it is really necessary to declare this
        widgets = {'color': ColorWidget}


class DifficultyLevelForm(ModelForm):
    class Meta:
        model = DifficultyLevel
        fields = ['color', 'level']
        widgets = {'color': DifficultyLevelWidget,
                   'level': HiddenInput}


class DifficultyLevelFormset(BaseInlineFormSet):
    def __init__(self, **kwargs):
        super().__init__(initial=[{'level': 0}], **kwargs)


DifficultyLevelFormset = inlineformset_factory(
    parent_model=Gym,
    model=DifficultyLevel,
    form=DifficultyLevelForm,
    formset=DifficultyLevelFormset,
    extra=1,
    can_delete=False,
)


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
