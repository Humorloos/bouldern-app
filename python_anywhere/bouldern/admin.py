"""This file is the home of model representations in the admin interface"""
from django.contrib.admin import site
from simple_history.admin import SimpleHistoryAdmin

from python_anywhere.bouldern.models import Boulder, Gym, Color, Grade, \
    Ascent, FavoriteGym

site.register(Color, SimpleHistoryAdmin)
site.register(Boulder, SimpleHistoryAdmin)
site.register(Grade, SimpleHistoryAdmin)
site.register(Gym, SimpleHistoryAdmin)
site.register(Ascent, SimpleHistoryAdmin)
site.register(FavoriteGym, SimpleHistoryAdmin)
