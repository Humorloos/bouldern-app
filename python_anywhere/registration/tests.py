"""Tests for registration app"""

from django.test import TestCase
from django.urls import reverse
from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory

from python_anywhere.registration.models import User
from python_anywhere.registration.views import UserDeleteView


class UserFactory(DjangoModelFactory):
    """Factory for building difficulty level instances"""

    class Meta:
        model = User

    email = 'testmail@mailprovider.com'
    username = 'myUserName'
    password = PostGenerationMethodCall('set_password', 'password')


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
