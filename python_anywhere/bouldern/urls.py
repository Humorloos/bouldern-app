"""URL mappings for bouldern app"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:gym>/map/', views.gym_map, name='map'),
]
