import pytest
from faker import Faker
from rest_framework.test import APIClient

from python_anywhere.accounts.factories import UserFactory

default_colors = {
    'Yellow': '#f6c026',
    'Red': '#d60000',
    'Green': '#0b8043',
    'Blue': '#039be5',
    'Orange': '#f5511d',
    'Purple': '#8e24aa',
    'White': '#eeede9',
    'Black': '#000000',
}


@pytest.fixture()
def logged_in_client(db):
    # login
    password = Faker().password()
    user = UserFactory(password=password)
    client = APIClient()
    client.login(username=user.email, password=password)
    yield client, user


@pytest.fixture()
def colors(db):
    from python_anywhere.bouldern.factories import ColorFactory
    yield [ColorFactory(name=name, color=color) for name, color in
           default_colors.items()]
