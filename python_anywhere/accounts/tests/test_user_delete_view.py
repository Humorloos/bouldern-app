"""Tests for user delete view"""
import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.status import HTTP_204_NO_CONTENT

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.accounts.models import User
from python_anywhere.accounts.views import UserDeleteView, UserAPI


def test_delete(client, db):
    """
    Test that requesting delete user view results in deletion of calling user
    """
    # given
    password = Faker().password()
    user = UserFactory(password=password)
    client.login(username=user.email, password=password)
    # when
    client.post(reverse(UserDeleteView.name))
    # then
    # noinspection PyTypeChecker
    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=user.pk)


def test_delete_api(logged_in_client_rest):
    # given
    client, user = logged_in_client_rest
    # when
    response = client.delete(UserAPI().reverse_action('detail', args=[user.id]))
    # then
    assert response.status_code == HTTP_204_NO_CONTENT
    assert len(User.objects.all()) == 0
