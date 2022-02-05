"""Tests for bouldern app"""
from django.utils.http import urlencode
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.models import Boulder, Ascent
from python_anywhere.bouldern.views import BoulderAPI, AscentAPI


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
        'grade_id': boulder_stub.grade.pk,
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
    assert boulder.grade == boulder_stub.grade


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


def test_ascent_api_post(logged_in_client_rest, colors):
    """Test that post method works correctly"""
    # Given
    client, user = logged_in_client_rest

    from python_anywhere.bouldern.factories import BoulderFactory
    boulder = BoulderFactory()

    from python_anywhere.bouldern.factories import AscentFactory
    ascent_stub = AscentFactory.stub(boulder=boulder)

    # When
    response = client.post(
        AscentAPI().reverse_action('list', args=[boulder.gym.pk, boulder.pk]),
        data={'result': ascent_stub.result}, format='json')

    # Then
    assert response.status_code == HTTP_201_CREATED
    ascent = Ascent.objects.first()
    assert ascent.created_by == user
    assert ascent.result == ascent_stub.result
    assert ascent.boulder == boulder


def test_ascent_api_put(logged_in_client_rest, colors):
    """Test that put method works correctly"""
    # Given
    client, user = logged_in_client_rest

    from python_anywhere.bouldern.factories import AscentFactory
    ascent = AscentFactory(result=Ascent.PROJECT)

    boulder = ascent.boulder

    # When
    response = client.put(
        AscentAPI().reverse_action(
            'detail', args=[boulder.gym.pk, boulder.pk, ascent.pk]),
        data={'result': Ascent.TOP}, format='json')

    # Then
    assert response.status_code == HTTP_200_OK
    ascent = Ascent.objects.first()
    assert ascent.created_by == user
    assert ascent.result == Ascent.TOP
    assert ascent.boulder == boulder


def test_ascent_api_get(logged_in_client_rest, colors):
    """Test that get method works correctly"""
    # Given
    client, user = logged_in_client_rest

    from python_anywhere.bouldern.factories import AscentFactory
    ascent = AscentFactory()
    boulder = ascent.boulder

    other_user = UserFactory()
    ascent_by_other_user = AscentFactory(created_by=other_user,
                                         boulder=boulder)

    ascent_in_other_gym = AscentFactory()

    old_ascent = AscentFactory(
        boulder__is_active=False,
        boulder__gym=boulder.gym,
    )

    # When
    response = client.get(
        AscentAPI().reverse_action('list', args=[boulder.gym.pk, '_']))

    # Then
    assert response.status_code == HTTP_200_OK
    ascents = set(response.data.serializer.instance)
    assert ascents == {ascent}
    assert ascent_by_other_user not in ascents
    assert ascent_in_other_gym not in ascents
    assert old_ascent not in ascents
