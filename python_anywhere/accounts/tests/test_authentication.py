from dj_rest_auth.utils import jwt_encode
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK


def test_refresh(logged_in_client):
    """Test that access token refresh endpoint works"""
    # given
    client, user = logged_in_client
    # when
    response = client.post(reverse('token_refresh'),
                           data={'refresh': str(jwt_encode(user)[1])})
    # then
    assert response.status_code == HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
