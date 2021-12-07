import json

from django import template

register = template.Library()


@register.filter
def serialize(formset):
    return json.dumps([{
        'options': [{
            'label': choice[1],
            'style': {'color': choice[0].instance.color},
            'value': choice[0].value
        } for choice in form.fields['color'].choices],
        'id': form.auto_id % form.prefix}
        for form in formset.forms])
