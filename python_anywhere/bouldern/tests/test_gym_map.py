"""Tests for bouldern app"""
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from python_anywhere.bouldern.models import Boulder
from python_anywhere.bouldern.views import BoulderAPI


def test_boulder_api_post(logged_in_client_rest, colors):
    """Test that post method works correctly"""
    # Given
    client, user = logged_in_client_rest

    from python_anywhere.bouldern.factories import GymFactory
    gym = GymFactory()

    from python_anywhere.bouldern.factories import BoulderFactory
    boulder_stub = BoulderFactory.stub(gym=gym)
    payload = {f'coordinates': boulder_stub.coordinates.geojson}
    payload.update({
        key: boulder_stub.__dict__[key].pk for key in ['color', 'difficulty']
    })
    # When
    response = client.post(BoulderAPI().reverse_action('list', args=[gym.pk]),
                           data=payload, format='json')
    # Then
    assert response.status_code == HTTP_201_CREATED
    boulder = Boulder.objects.first()
    assert boulder.created_by == user
    assert boulder.coordinates.geojson == payload['coordinates']
    assert boulder.gym == gym
    assert boulder.color == boulder_stub.color
    assert boulder.difficulty == boulder_stub.difficulty


def test_boulder_api_get(logged_in_client_rest, colors):
    client, user = logged_in_client_rest
    from python_anywhere.bouldern.factories import GymFactory
    correct_gym = GymFactory()
    incorrect_gym = GymFactory()
    from python_anywhere.bouldern.factories import BoulderFactory
    correct_boulders = {BoulderFactory(gym=correct_gym) for _ in range(3)}
    incorrect_boulders = {BoulderFactory(gym=incorrect_gym) for _ in range(3)}
    # when
    response = client.get(
        BoulderAPI().reverse_action('list', args=[correct_gym.pk]))
    # then
    assert response.status_code == HTTP_200_OK
    boulders = set(response.data.serializer.instance)
    assert boulders.intersection(correct_boulders) == boulders
    assert boulders.intersection(incorrect_boulders) == set()
