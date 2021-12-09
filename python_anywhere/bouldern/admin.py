"""This file is the home of model representations in the admin interface"""
from django.contrib import admin

from python_anywhere.bouldern.models import Boulder, Gym, Color, DifficultyLevel

# todo: check if this can be replaced by just site.register()
admin.site.register(Color)
admin.site.register(Boulder)
admin.site.register(DifficultyLevel)
admin.site.register(Gym)
