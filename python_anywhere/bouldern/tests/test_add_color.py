from dj_rest_auth.utils import jwt_encode
from django.urls import reverse
from faker import Faker
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APIClient

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.accounts.models import User
from python_anywhere.bouldern.models import Color
from python_anywhere.bouldern.views import AddGym, AddColor, AddColorRest


def test_add_color(client, db):
    """Test that post method works correctly"""
    # Given
    # login
    password = Faker().password()
    user = UserFactory(password=password)
    client.login(username=user.email, password=password)

    from python_anywhere.bouldern.factories import ColorFactory
    payload = {key: ColorFactory.stub().__dict__[key]
               for key in ['color', 'name']}

    # When
    response = client.post(reverse(AddColor.name), data=payload)

    # Then
    color = Color.objects.first()
    assert color.name == payload['name']
    assert color.color == payload['color']
    assert color.created_by == user
    assert response.url == reverse(AddGym.name)


def test_add_color_rest(logged_in_client_rest):
    """Test that post method works correctly"""
    # Given
    client, user = logged_in_client_rest

    from python_anywhere.bouldern.factories import ColorFactory
    payload = {key: ColorFactory.stub().__dict__[key]
               for key in ['color', 'name']}

    # When
    response = client.post(reverse('color-list'), data=payload,
                           format='json')
    # Then
    assert response.status_code == HTTP_201_CREATED
    color = Color.objects.first()
    assert color.name == payload['name']
    assert color.color == payload['color']
    assert color.created_by == user
