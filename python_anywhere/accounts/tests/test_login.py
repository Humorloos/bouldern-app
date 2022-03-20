import datetime

import pandas as pd
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

    payload = {'email': user.email, 'password': password}

    # When
    response = client.post(reverse('rest_login'), data=payload, format='json')

    # Then
    assert response.status_code == HTTP_200_OK
    user_data = response.data['user']
    assert user_data['username'] == user.username
    assert user_data['email'] == user.email

    assert (pd.Timestamp(response.data['refresh_token_expiration']).date() -
            datetime.date.today()).days == 7

    request = HttpRequest()
    request.META['HTTP_AUTHORIZATION'] = \
        f"Bearer {response.data['access_token']}"
    logged_in_user, _ = JWTCookieAuthentication().authenticate(request)
    assert logged_in_user == user


def test_cannot_login_with_inactive_user(db):
    """Test that users whose account was deactivated cannot login"""
    # Given
    client = APIClient()
    password = Faker().password()
    user = UserFactory(password=password, is_active=False)

    payload = {'email': user.email, 'password': password}

    # When
    response = client.post(reverse('rest_login'), data=payload, format='json')

    # Then
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_cannot_login_with_unverified_user(db):
    """Test that users whose email has not been verified cannot log in"""
    # Given
    client = APIClient()
    password = Faker().password()
    user = UserFactory(password=password, verified=False)

    payload = {'email': user.email, 'password': password}

    # When
    response = client.post(reverse('rest_login'), data=payload, format='json')

    # Then
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_can_login_with_uppercase_email(db):
    """
    Test that users can login when they use upper case characters in their email
    """
    # Given
    client = APIClient()
    password = Faker().password()
    user = UserFactory(password=password, email='myemail@provider.com')

    payload = {
        'email': user.email.upper(),
        'password': password
    }

    # When
    response = client.post(reverse('rest_login'), data=payload, format='json')

    # Then
    assert response.status_code == HTTP_200_OK
