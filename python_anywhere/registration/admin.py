from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin

from python_anywhere.registration.models import User

site.register(User, UserAdmin)
