"""URL mappings for bouldern app"""
from django.urls import path

from .views import index, gym_map, AddGym, AddColor

urlpatterns = [
    path('', index, name='index'),
    path('<str:gym>/map/', gym_map, name='map'),
    path('add-color/', AddColor.as_view(), name=AddColor.name),
    path('add-gym/', AddGym.as_view(), name=AddGym.name),
]
