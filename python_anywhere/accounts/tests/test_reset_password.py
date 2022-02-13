from django.core import mail
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from python_anywhere.accounts.factories import UserFactory


def test_reset_password(db):
    """Test that users receive a password reset mail when requesting one"""
    # Given
    client = APIClient()
    user = UserFactory()
    payload = {'email': user.email}

    # When
    response = client.post(reverse('rest_password_reset'), data=payload,
                           format='json')
    # Then
    assert response.status_code == HTTP_200_OK
    assert 'password reset' in mail.outbox[0].body

    # Given
    reset_url_components = response.context[0].get('password_reset_url')\
        .split('/')
    token = reset_url_components[-2]
    uid = reset_url_components[-3]
    password = Faker().password()
    confirm_payload = {
        'token': token,
        'uid': uid,
        'new_password1': password,
        'new_password2': password
    }

    # When
    response = client.post(reverse('rest_password_reset_confirm'),
                           data=confirm_payload, format='json')

    # Then
    assert response.status_code == HTTP_200_OK
    assert client.login(username=user.email, password=password)
