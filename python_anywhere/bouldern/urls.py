"""URL mappings for bouldern app"""
from django.urls import path
from django.views.generic import TemplateView

from python_anywhere.bouldern.views import gym_map, AddGym, AddColor, AddGymRest

urlpatterns = [
    path('', TemplateView.as_view(template_name='bouldern/index.html'),
         name='index'),
    path('<str:gym_name>/map/', gym_map, name='map'),
    path('add-color/', AddColor.as_view(), name=AddColor.name),
    path('add-gym/', AddGym.as_view(), name=AddGym.name),
    path('rest/add-gym/', AddGymRest.as_view(), name=AddGymRest.name),
]
