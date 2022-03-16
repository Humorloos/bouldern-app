from allauth.account.adapter import DefaultAccountAdapter

from python_anywhere.accounts.models import User


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        if not commit:
            inactive_user_id = User.all_objects\
                .filter(is_active=False, email=user.email).values('id').first()
            if inactive_user_id is not None:
                user.pk = inactive_user_id['id']
        return user
