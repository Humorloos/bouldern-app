"""This file contains views for the registration app"""

# registration/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView

from python_anywhere.registration.forms import EmailUserCreationForm


class SignUpView(CreateView):
    """View for user sign up"""
    form_class = EmailUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
