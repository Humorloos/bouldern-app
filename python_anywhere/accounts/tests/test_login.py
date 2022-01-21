from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.http import HttpRequest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
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
    request.META['HTTP_AUTHORIZATION'] = \
        f"Bearer {response.data['access_token']}"
    logged_in_user, _ = JWTCookieAuthentication().authenticate(request)
    assert logged_in_user == user


def test_cannot_login_with_inactive_user(db):
    """Test that users can login"""
    # Given
    client = APIClient()
    password = Faker().password()
    user = UserFactory(password=password, is_active=False)

    payload = {'username': user.__dict__['email'], 'password': password}

    # When
    response = client.post(reverse('rest_login'), data=payload, format='json')

    # Then
    assert response.status_code == HTTP_400_BAD_REQUEST
