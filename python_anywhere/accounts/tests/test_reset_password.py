from django.core import mail
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
