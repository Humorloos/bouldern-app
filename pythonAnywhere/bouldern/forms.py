from django.forms import ModelForm, formset_factory, TextInput

from .models import Boulder


class BoulderForm(ModelForm):
    class Meta:
        model = Boulder
        fields = ['coordinates']
        widgets = {
            'coordinates': TextInput,
        }


GymMapFormSet = formset_factory(BoulderForm, extra=1)
