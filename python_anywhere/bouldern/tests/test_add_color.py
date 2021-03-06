from django.urls import reverse
from faker import Faker
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from python_anywhere.bouldern.models import Color
from python_anywhere.bouldern.views import ColorAPI


def test_color_api_post(logged_in_client):
    """Test that post method works correctly"""
    # Given
    client, user = logged_in_client

    from python_anywhere.bouldern.factories import ColorFactory
    payload = {key: ColorFactory.build().__dict__[key]
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


def test_color_api_get(logged_in_client):
    """Test that post method works correctly"""
    # Given
    client, user = logged_in_client

    from python_anywhere.bouldern.factories import ColorFactory
    faker = Faker()
    colors = [ColorFactory(name=faker.unique.color()) for _ in range(3)]

    # When
    response = client.get(ColorAPI().reverse_action('list'))
    # Then
    assert response.status_code == HTTP_200_OK
    for instance in response.data.serializer.instance:
        assert instance in colors
