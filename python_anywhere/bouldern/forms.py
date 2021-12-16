"""This module contains forms for the bouldern app"""
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet, \
    HiddenInput, BaseInlineFormSet, ModelChoiceField
from django.forms import inlineformset_factory

from python_anywhere.bouldern.models import Boulder, Gym, Color, DifficultyLevel
from python_anywhere.bouldern.widgets import CoordinatesWidget


class UGCForm(ModelForm):
    def save_for_user(self, user):
        ugc = super().save()
        ugc.created_by = user
        ugc.save()


class GymForm(UGCForm):
    """Form for adding new bouldering gyms"""

    class Meta:
        model = Gym
        fields = ['name', 'map']


class ColorForm(UGCForm):
    """Form for adding new colors"""

    class Meta:
        model = Color
        fields = ['name', 'color']


class DifficultyLevelForm(UGCForm):
    """Form for adding new difficulty levels"""
    color = ModelChoiceField(Color.objects.all(), empty_label=None,
                             widget=HiddenInput)

    class Meta:
        model = DifficultyLevel
        fields = ['level', 'color']
        widgets = {'level': HiddenInput}


class BaseDifficultyLevelFormset(BaseInlineFormSet):
    """Base class for difficulty level form set"""

    def __init__(self, **kwargs):
        super().__init__(initial=[{'level': 0}], **kwargs)


DifficultyLevelFormset = inlineformset_factory(
    parent_model=Gym,
    model=DifficultyLevel,
    form=DifficultyLevelForm,
    formset=BaseDifficultyLevelFormset,
    extra=1,
    can_delete=False,
)


class BoulderForm(UGCForm):
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
