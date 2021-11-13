"""This file is the home of model representations in the admin interface"""
from django.contrib import admin

from .models import Boulder

admin.site.register(Boulder)
