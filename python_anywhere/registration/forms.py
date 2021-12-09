from django.contrib.auth.forms import UserCreationForm, UsernameField

from python_anywhere.registration.models import User


class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}
