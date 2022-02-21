"""Tests for bouldern app"""
from django.utils.http import urlencode
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, \
    HTTP_204_NO_CONTENT

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.models import Boulder, Ascent
from python_anywhere.bouldern.views import BoulderAPI, AscentAPI, \
    GymMapResourcesAPI


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
    boulder_creator = UserFactory()
    client, user = logged_in_client_rest
    from python_anywhere.bouldern.factories import BoulderFactory
    boulder_2_retire = BoulderFactory(created_by=boulder_creator)
    active_boulders = {BoulderFactory(gym=boulder_2_retire.gym)
                       for _ in range(3)}
    # when
    response = client.delete(
        BoulderAPI().reverse_action(
            'detail', args=[boulder_2_retire.gym.pk, boulder_2_retire.pk]),
        format='json')
    # then
    assert response.status_code == HTTP_204_NO_CONTENT
    retired_boulder = Boulder.objects.get(pk=boulder_2_retire.pk)
    assert not retired_boulder.is_active
    assert retired_boulder.modified_by == user
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


def test_gym_map_resources_api_get(colors, logged_in_client_rest):
    client, user = logged_in_client_rest
    incorrect_user = UserFactory()

    from python_anywhere.bouldern.factories import GymFactory
    correct_gym = GymFactory()
    from python_anywhere.bouldern.factories import GradeFactory
    incorrect_gym = GymFactory()
    undefined_grade = GradeFactory(gym=correct_gym, grade=None)

    from python_anywhere.bouldern.factories import BoulderFactory
    correct_boulders_without_ascent = BoulderFactory \
        .create_batch(3, gym=correct_gym)

    boulders_in_other_gym = BoulderFactory.create_batch(3, gym=incorrect_gym)
    inactive_boulder = BoulderFactory(gym=correct_gym, is_active=False)

    from python_anywhere.bouldern.factories import AscentFactory
    correct_ascents = AscentFactory.create_batch(3, boulder__gym=correct_gym,
                                                 created_by=user)
    correct_boulders = [a.boulder for a in correct_ascents]

    [AscentFactory(created_by=user, boulder=b, is_active=False) for b in
     correct_boulders]

    [AscentFactory(created_by=incorrect_user, boulder=b) for b in
     correct_boulders]

    response = client.get(f'{GymMapResourcesAPI().reverse_action("list")}?'
                          f'{urlencode({"name": correct_gym.name})}')
    # then
    assert response.status_code == HTTP_200_OK
    # verify gym
    response_data = response.data.serializer.instance
    assert response_data['gym'] == correct_gym
    assert response.data['gym']['grade_set'][-1]['grade'] == 'undefined'
    # verify boulder features
    response_boulders = {bf['boulder']
                         for bf in response_data['boulder_features']}
    response_ascents = {bf['boulder'].pk: bf['ascent']
                        for bf in response_data['boulder_features']}
    assert all(
        b in response_boulders and response_ascents[b.pk] is None
        for b in correct_boulders_without_ascent)
    assert all(
        b in response_boulders
        and response_ascents[b.pk] in correct_ascents
        for b in correct_boulders)
    assert not any(b in response_boulders for b in boulders_in_other_gym)
    assert inactive_boulder not in response_boulders
