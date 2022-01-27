"""Tests for bouldern app"""
from django.utils.http import urlencode
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
        'color_id': boulder_stub.color.pk,
        'difficulty_id': boulder_stub.difficulty.pk,
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
    inactive_boulder = {BoulderFactory(gym=correct_gym, is_active=False)}
    # when
    response = client.get(
        f'{BoulderAPI().reverse_action("list", args=[correct_gym.pk])}?'
        f'{urlencode({"is_active": True})}')
    # then
    assert response.status_code == HTTP_200_OK
    boulders = set(response.data.serializer.instance)
    assert boulders.intersection(correct_boulders) == boulders
    assert boulders.intersection(incorrect_boulders) == set()
    assert inactive_boulder not in boulders


def test_boulder_api_retire(logged_in_client_rest, colors):
    client, user = logged_in_client_rest
    from python_anywhere.bouldern.factories import BoulderFactory
    boulder_2_retire = BoulderFactory()
    active_boulders = {BoulderFactory(gym=boulder_2_retire.gym)
                       for _ in range(3)}
    # when
    response = client.patch(
        BoulderAPI().reverse_action(
            'detail', args=[boulder_2_retire.gym.pk, boulder_2_retire.pk]),
        data={'is_active': False},
        format='json')
    # then
    assert response.status_code == HTTP_200_OK
    assert not Boulder.objects.get(pk=boulder_2_retire.pk).is_active
    assert all(b.is_active for b in Boulder.objects.filter(
        pk__in={b.pk for b in active_boulders}))
