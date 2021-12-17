"""
This script contains factories for building model instances of the registration
app
"""

from factory import PostGenerationMethodCall, Faker
from factory.django import DjangoModelFactory

from python_anywhere.registration.models import User


class UserFactory(DjangoModelFactory):
    """Factory for building difficulty level instances"""

    class Meta:
        model = User

    email = Faker('email')
    username = Faker('user_name')
    password = PostGenerationMethodCall('set_password', 'password')

    is_superuser = False
    is_staff = False
