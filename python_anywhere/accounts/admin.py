"""File for regisration of default User model in admin"""

from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin

from python_anywhere.accounts.models import User

site.register(User, UserAdmin)
