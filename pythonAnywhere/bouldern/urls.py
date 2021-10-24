from django.urls import path

from . import views
from .constants import BOULDER_ISLAND_URI, STUDIO_BLOC_URI

urlpatterns = [
    path('', views.index, name='index'),
    path(f'{BOULDER_ISLAND_URI}', views.index, name='index'),
    path(f'{STUDIO_BLOC_URI}', views.index, name='index'),
]
