from django.contrib.auth.models import UserManager


class OnlyActiveManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
