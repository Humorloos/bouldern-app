import json

from django import template

register = template.Library()


@register.filter
def serialize(optgroups):
    return json.dumps([
        {'label': optgroup[1][0]['value'].instance.name,
         'style': {'color': optgroup[1][0]['value'].instance.color}}
        for optgroup in optgroups])
