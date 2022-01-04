"""Tests for bouldern app"""
import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.models import Boulder
from python_anywhere.bouldern.views import gym_map, BoulderAPI


@pytest.mark.django_db
def test_gym_map(client):
    """Test that post path works correctly"""
    # Given
    # login
    password = Faker().password()
    user = UserFactory(password=password)
    client.login(username=user.email, password=password)

    from python_anywhere.bouldern.factories import GymFactory
    gym = GymFactory()
    n_boulders = 3

    boulder_prefix = "boulder-"
    payload = {f'{boulder_prefix}TOTAL_FORMS': str(n_boulders),
               f'{boulder_prefix}INITIAL_FORMS': '0'}

    from python_anywhere.bouldern.factories import BoulderFactory
    boulders_payload = {f'{boulder_prefix}{i}-coordinates': BoulderFactory.stub(
        gym=gym).coordinates.geojson for i in range(n_boulders)}
    payload.update(boulders_payload)

    # When
    response = client.post(
        reverse(gym_map, kwargs={'gym_name': gym.name}),
        data=payload)

    # Then
    boulders = Boulder.objects.all()
    for boulder in boulders:
        assert boulder.created_by == user
        assert boulder.coordinates.geojson in boulders_payload.values()
        assert boulder.gym == gym
    assert response.url == reverse(gym_map, kwargs={'gym_name': gym.name})


def test_boulder_api_post(logged_in_client_rest):
    """Test that post method works correctly"""
    # Given
    client, user = logged_in_client_rest

    from python_anywhere.bouldern.factories import GymFactory
    gym = GymFactory()

    from python_anywhere.bouldern.factories import BoulderFactory
    payload = {f'coordinates': BoulderFactory.stub(
        gym=gym).coordinates.geojson, 'gym': gym.pk}
    # When
    response = client.post(BoulderAPI().reverse_action('list', args=[gym.pk]),
                           data=payload, format='json')
    # Then
    assert response.status_code == HTTP_201_CREATED
    boulder = Boulder.objects.first()
    assert boulder.created_by == user
    assert boulder.coordinates.geojson == payload['coordinates']
    assert boulder.gym == gym


def test_boulder_api_get(logged_in_client_rest):
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
