from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.http import HttpRequest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from python_anywhere.accounts.factories import UserFactory


def test_login(db):
    """Test that users can login"""
    # Given
    client = APIClient()
    password = Faker().password()
    user = UserFactory(password=password)

    payload = {'username': user.__dict__['email'], 'password': password}

    # When
    response = client.post(reverse('rest_login'), data=payload, format='json')

    # Then
    request = HttpRequest()
    request.COOKIES['auth-token'] = response.cookies['auth-token'].value
    logged_in_user, _ = JWTCookieAuthentication().authenticate(request)
    assert logged_in_user == user
