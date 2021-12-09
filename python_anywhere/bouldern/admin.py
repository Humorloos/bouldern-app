"""This file is the home of model representations in the admin interface"""
from django.contrib.admin import site

from python_anywhere.bouldern.models import Boulder, Gym, Color, DifficultyLevel

site.register(Color)
site.register(Boulder)
site.register(DifficultyLevel)
site.register(Gym)
