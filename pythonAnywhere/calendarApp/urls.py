from django.urls import path

from . import views

urlpatterns = [
    path('', views.handle_calendar_update, name='calendar update handler'),
]
