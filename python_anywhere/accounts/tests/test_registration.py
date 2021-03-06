from allauth.account.models import EmailAddress
from django.core import mail
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APIClient

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.accounts.models import User


def test_register(db):
    """Test that users can register"""
    # Given
    client = APIClient()
    password = Faker().password()
    user = UserFactory.build(password=password)
    payload = {key: user.__dict__[key] for key in ['username', 'email']}
    payload.update({f'password{i}': password for i in range(1, 3)})

    # When
    response = client.post(reverse('rest_register'), data=payload,
                           format='json')
    # Then
    assert len(mail.outbox) == 1
    assert response.status_code == HTTP_201_CREATED
    created_user = User.objects.first()
    assert created_user.email == payload['email']
    assert created_user.username == payload['username']
    assert created_user.check_password(password)


# noinspection DuplicatedCode
def test_lower_case_email(db):
    """
    Test that emails used in registration are transformed to lower case.
    """
    # Given
    client = APIClient()
    password = Faker().password()
    user = UserFactory.build(password=password, email='Myemail@provider.com')
    payload = {key: user.__dict__[key] for key in ['username', 'email']}
    payload.update({f'password{i}': password for i in [1, 2]})

    # When
    response = client.post(reverse('rest_register'), data=payload,
                           format='json')
    # Then
    assert response.status_code == HTTP_201_CREATED
    created_user = User.objects.first()
    assert created_user.email == payload['email'].lower()


# noinspection DuplicatedCode
def test_inactive_user(db):
    """Test that users that were deleted can register again"""
    # Given
    client = APIClient()
    password = Faker().password()
    # inactive user because she was deleted
    user = UserFactory(password=password, email='myemail@provider.com',
                       is_active=False)
    # delete email address because user was deleted
    EmailAddress.objects.first().delete()

    payload = {key: user.__dict__[key] for key in ['username', 'email']}
    payload.update({f'password{i}': password for i in [1, 2]})

    # When
    response = client.post(reverse('rest_register'), data=payload,
                           format='json')
    # Then
    assert response.status_code == HTTP_201_CREATED
    created_user = User.objects.first()
    assert created_user.username == user.username
    assert created_user.email == user.email
    email = EmailAddress.objects.first()
    assert email.email == user.email
