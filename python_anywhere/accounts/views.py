"""This file contains views for the accounts app"""

# accounts/views.py
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView
from rest_framework.mixins import DestroyModelMixin

from python_anywhere.accounts.forms import EmailUserCreationForm
from python_anywhere.accounts.models import User
from python_anywhere.accounts.serializers import UserSerializer
from python_anywhere.views import ReversibleViewSet


class SignUpView(CreateView):
    """View for user sign up"""
    form_class = EmailUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserDeleteView(DeleteView):
    """View for user account deletion"""
    name = 'quit'
    model = User

    def delete(self, request, *args, **kwargs):
        User.objects.get(pk=request.user.pk).delete()
        return HttpResponseRedirect(reverse('index'))


class UserAPI(ReversibleViewSet, DestroyModelMixin):
    """Rest API for reading and creating boulders in a specific gym"""
    basename = 'user'
    queryset = User.objects.all()
    serializer_class = UserSerializer
