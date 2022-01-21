"""Tests for user delete view"""
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from python_anywhere.accounts.models import User
from python_anywhere.accounts.views import UserAPI


def test_delete(logged_in_client_rest):
    # given
    client, user = logged_in_client_rest
    # when
    response = client.patch(UserAPI().reverse_action('detail', args=[user.id]),
                            data={'is_active': False})

    # then
    assert response.status_code == HTTP_200_OK
    user = User.objects.first()
    assert not user.is_active
