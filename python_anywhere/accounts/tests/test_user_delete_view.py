"""Tests for user delete view"""
import pytest
from django.urls import reverse
from faker import Faker

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.accounts.models import User
from python_anywhere.accounts.views import UserDeleteView


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
