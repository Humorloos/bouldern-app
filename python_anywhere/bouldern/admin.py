"""This file is the home of model representations in the admin interface"""
from django.contrib import admin

from .models import Boulder, Gym, Color, DifficultyLevel

admin.site.register(Color)
admin.site.register(Boulder)
admin.site.register(DifficultyLevel)
admin.site.register(Gym)
