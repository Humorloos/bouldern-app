import json

from django import template
from django.utils.safestring import SafeString

register = template.Library()


def render_without_field(form, excluded):
    return '\n'.join(str(value.get_bound_field(form, key))
                     for key, value in form.fields.items()
                     if key != excluded)


@register.filter
def serialize(formset):
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
def without_total_forms(management_form):
    return SafeString(render_without_field(management_form, 'TOTAL_FORMS'))
