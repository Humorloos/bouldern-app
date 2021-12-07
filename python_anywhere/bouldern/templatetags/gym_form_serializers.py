"""Serializers for gym_form template"""
import json

from django import template
from django.forms import BaseForm, BaseFormSet
from django.forms.formsets import ManagementForm
from django.utils.safestring import SafeString

register = template.Library()


def render_without_field(form: BaseForm, excluded: str) -> str:
    """
    Renders html for provided form without the provided field.
    :param form: form to render html for
    :param excluded: field not to include in the rendered html text
    :return: html text
    """
    return '\n'.join(str(value.get_bound_field(form, key))
                     for key, value in form.fields.items()
                     if key != excluded)


@register.filter
def difficulty_level_select_data(formset: BaseFormSet) -> str:
    """
    Gets the data for populating the diffculty level select components in the
    gym form component.
    :param formset: difficulty level formset containing the required data
    :return: json representation of data
    """
    return json.dumps([{
        'options': [{
            'label': choice[1],
            'style': {'color': choice[0].instance.color},
            'value': choice[0].value
        } for choice in form.fields['color'].choices],
        'prefix': form.prefix,
        'html': render_without_field(form, 'color')
    } for form in formset])


@register.filter
def without_total_forms(management_form: ManagementForm) -> SafeString:
    """
    Gets html text of provided management form, excluding the total forms field.
    :param management_form: management form to serialize
    :return: html text as safe string
    """
    return SafeString(render_without_field(management_form, 'TOTAL_FORMS'))
