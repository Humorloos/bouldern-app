"""URL mappings for bouldern app"""
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from python_anywhere.bouldern.views import gym_map, AddGym, AddColor, \
    GymAPI, ColorAPI, BoulderAPI

router = SimpleRouter()
router.register(GymAPI.basename, GymAPI)
router.register(ColorAPI.basename, ColorAPI)

gym_router = NestedSimpleRouter(router, GymAPI.basename,
                                lookup=GymAPI.basename)
gym_router.register(BoulderAPI.basename, BoulderAPI)

urlpatterns = [
    path('', TemplateView.as_view(template_name='bouldern/index.html'),
         name='index'),
    path('<str:gym_name>/map/', gym_map, name='map'),
    path('add-color/', AddColor.as_view(), name=AddColor.name),
    path('add-gym/', AddGym.as_view(), name=AddGym.name),
] + router.urls + gym_router.urls
