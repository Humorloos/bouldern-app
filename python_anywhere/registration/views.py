"""This file contains views for the registration app"""

# registration/views.py
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView

from python_anywhere.registration.forms import EmailUserCreationForm
from python_anywhere.registration.models import User


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
