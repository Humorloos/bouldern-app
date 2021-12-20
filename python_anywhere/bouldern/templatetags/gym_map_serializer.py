"""Serializers for Gym Map template"""
import json

from django import template
from django.db.models.fields.files import ImageFieldFile

from python_anywhere.bouldern.forms import GymMapFormSet

register = template.Library()


@register.filter
def gym_map_data(gym_map: ImageFieldFile) -> str:
    """
    Gets relevant properties for image layer in Gym Map vue component
    :param gym_map: the gym's image field to get the properties of
    :return: json representation of properties required for image layer
    """
    return json.dumps({
        'height': gym_map.height,
        'width': gym_map.width,
        'path': gym_map.url,
    })


@register.filter
def boulder_coordinates(formset: GymMapFormSet) -> str:
    """
    Gets boulder coordinates from provided GymMapFormSet
    :param formset: GymMapFormSet containing the boulder coordinates
    :return: json representation of list of geoJson boulder coordinates
    """
    return json.dumps([form.initial['coordinates'].geojson for form in formset])
