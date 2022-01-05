"""Tests for user delete view"""
from rest_framework.status import HTTP_204_NO_CONTENT

from python_anywhere.accounts.models import User
from python_anywhere.accounts.views import UserAPI


def test_delete(logged_in_client_rest):
    # given
    client, user = logged_in_client_rest
    # when
    response = client.delete(UserAPI().reverse_action('detail', args=[user.id]))
    # then
    assert response.status_code == HTTP_204_NO_CONTENT
    assert len(User.objects.all()) == 0
