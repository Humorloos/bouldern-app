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
        'color': boulder_stub.color.pk,
        'grade': boulder_stub.grade.pk,
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


def test_ascent_api_post_new_ascent(logged_in_client_rest, colors):
    """Test that post method creates new ascents"""
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


def test_ascent_api_post_existing_ascent(logged_in_client_rest, colors):
    """
    Test that post method sets existing ascents inactive when posting to
    the same boulder for the same user
    """
    # Given
    client, user = logged_in_client_rest

    from python_anywhere.bouldern.factories import AscentFactory
    existing_ascent = AscentFactory(result=Ascent.PROJECT)

    boulder = existing_ascent.boulder

    # When
    response = client.post(
        AscentAPI().reverse_action('list', args=[boulder.gym.pk, boulder.pk]),
        data={'result': Ascent.TOP}, format='json')

    # Then
    assert response.status_code == HTTP_201_CREATED
    created_ascent = Ascent.objects.filter(is_active=True).first()
    assert created_ascent.created_by == user
    assert created_ascent.result == Ascent.TOP
    assert created_ascent.boulder == boulder
    existing_ascent = Ascent.objects.filter(is_active=False).first()
    assert existing_ascent.boulder == boulder
