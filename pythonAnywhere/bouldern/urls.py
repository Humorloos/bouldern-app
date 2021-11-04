from django.urls import path

from . import views

app_name = 'bouldern'
urlpatterns = [
    path('', views.index, name='index'),
    path(f'<str:gym>/map/', views.gym_map, name='map'),
]
