import pytest
from dj_rest_auth.utils import jwt_encode
from faker import Faker
from rest_framework.test import APIClient

from python_anywhere.accounts.factories import UserFactory


@pytest.fixture()
def logged_in_client(db):
    # login
    password = Faker().password()
    user = UserFactory(password=password)
    client = APIClient()
    client.login(username=user.email, password=password)
    yield client, user


@pytest.fixture()
def logged_in_client_rest(db):
    # login
    password = Faker().password()
    user = UserFactory(password=password)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(jwt_encode(user)[0]))
    yield client, user
