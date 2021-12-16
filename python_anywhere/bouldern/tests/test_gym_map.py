"""Tests for bouldern app"""
import pytest
from django.urls import reverse
from faker import Faker

from python_anywhere.bouldern.models import Boulder
from python_anywhere.bouldern.views import gym_map
from python_anywhere.registration.factories import UserFactory


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
        gym=gym).coordinates for i in range(n_boulders)}
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
