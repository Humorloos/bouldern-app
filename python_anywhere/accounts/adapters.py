"""This file contains custom django allauth adapters"""

from allauth.account.adapter import DefaultAccountAdapter

from python_anywhere.accounts.models import User


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Adapter for overriding inactive users instead of trying to create new ones
    """
    def save_user(self, request, user, form, commit=True):
        """
        When called with commit=False (which is the case in
        dj_rest_auth/registration/serializers.py:239), checks if inactive user
        with same email-address as provided user exists and assigns its id to
        make sure user is updated instead of inserted.
        """
        user = super().save_user(request, user, form, commit)
        if not commit:
            inactive_user_id = User.all_objects\
                .filter(is_active=False, email=user.email).values('id').first()
            if inactive_user_id is not None:
                user.pk = inactive_user_id['id']
        return user
