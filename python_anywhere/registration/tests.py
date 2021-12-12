"""Tests for registration app"""

from django.test import TestCase
from django.urls import reverse

from python_anywhere.registration.factories import UserFactory
from python_anywhere.registration.models import User
from python_anywhere.registration.views import UserDeleteView


class DeleteUserTest(TestCase):
    """Test for DeleteUser view"""

    def test_delete(self):
        """
        Test that requesting delete user view results in deletion of calling user
        """
        # given
        password = 'OAwIYQRCdiplaCIwEEcn'
        user = UserFactory(password=password)
        self.client.login(username=user.email, password=password)
        # when
        self.client.post(reverse(UserDeleteView.name))
        # then
        # noinspection PyTypeChecker
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user.pk)
