"""
This script contains factories for building model instances of the accounts
app
"""

from allauth.account.models import EmailAddress
from factory import PostGenerationMethodCall, Faker, RelatedFactory, \
    SelfAttribute
from factory.django import DjangoModelFactory

from python_anywhere.accounts.models import User


class EmailAddressFactory(DjangoModelFactory):
    """Factory for building email address instances"""

    class Meta:
        model = EmailAddress

    verified = 1
    primary = 1


class UserFactory(DjangoModelFactory):
    """Factory for building grade instances"""

    class Meta:
        model = User

    email = Faker('email')
    username = Faker('user_name')
    password = PostGenerationMethodCall('set_password', 'password')

    is_superuser = False
    is_staff = False

    related_email = RelatedFactory(
        EmailAddressFactory,
        factory_related_name='user',
        email=SelfAttribute('..email'),
    )
