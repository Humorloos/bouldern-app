import pytest
from faker import Faker
from rest_framework.test import APIClient

from python_anywhere.registration.factories import UserFactory


@pytest.fixture()
def logged_in_client(db):
    # login
    password = Faker().password()
    user = UserFactory(password=password)
    client = APIClient()
    client.login(username=user.email, password=password)
    yield client, user
