import json

from django import template
from django.db.models.fields.files import ImageFieldFile

register = template.Library()


@register.filter
def gym_map_data(gym_map: ImageFieldFile):
    return json.dumps({
        'height': gym_map.height,
        'width': gym_map.width,
        'path': gym_map.url,
    })


@register.filter
def boulder_coordinates(formset):
    return json.dumps([form.initial['coordinates'].geojson for form in formset])

