from django.forms import ModelForm, formset_factory, TextInput, BaseFormSet

from .models import Boulder


class BoulderForm(ModelForm):
    class Meta:
        model = Boulder
        fields = ['coordinates']
        widgets = {
            'coordinates': TextInput,
        }


class BaseGymMapFormSet(BaseFormSet):
    def __init__(self, **kwargs):
        super().__init__(prefix='boulder', **kwargs)


GymMapFormSet = formset_factory(BoulderForm, extra=0)
