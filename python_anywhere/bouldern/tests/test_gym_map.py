"""Tests for bouldern app"""
from django.contrib.gis.geos import Point
from django.utils.http import urlencode
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, \
    HTTP_204_NO_CONTENT

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.models import Boulder, Ascent
from python_anywhere.bouldern.tests.test_gym_api import grade_2_dict
from python_anywhere.bouldern.views import BoulderAPI, AscentAPI, \
    GymMapResourcesAPI


def test_boulder_api_post(logged_in_client, colors, gym, boulder):
    """Test that post method works correctly"""
    # Given
    client, user = logged_in_client
    boulder_gym = gym()

    boulder_stub = boulder.build(gym=boulder_gym)
    payload = {f'coordinates': boulder_stub.coordinates.geojson}
    payload.update({
        'color': boulder_stub.color.pk,
        'grade': boulder_stub.grade.pk,
    })
    # When
    response = client.post(
        BoulderAPI().reverse_action('list', args=[boulder_gym.pk]),
        data=payload, format='json')
    # Then
    assert response.status_code == HTTP_201_CREATED
    boulder = Boulder.objects.first()
    assert boulder.created_by == user
    assert boulder.coordinates.geojson == payload['coordinates']
    assert boulder.gym == boulder_gym
    assert boulder.color == boulder_stub.color
    assert boulder.grade == boulder_stub.grade


def test_boulder_api_retire(logged_in_client, colors, boulder):
    boulder_creator = UserFactory()
    client, user = logged_in_client
    boulder_2_retire = boulder(created_by=boulder_creator)
    active_boulders = {boulder(gym=boulder_2_retire.gym)
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


def test_boulder_api_move(logged_in_client, colors, boulder):
    boulder_creator = UserFactory()
    client, user = logged_in_client
    boulder_2_move = boulder(created_by=boulder_creator)
    new_position = Point(799, 645).geojson
    data = {'coordinates': new_position}
    # when
    # noinspection DuplicatedCode
    response = client.patch(
        BoulderAPI().reverse_action(
            'detail', args=[boulder_2_move.gym.pk, boulder_2_move.pk]),
        data=data, format='json')
    # then
    assert response.status_code == HTTP_200_OK
    boulder_2_move.refresh_from_db()
    assert boulder_2_move.modified_by == user
    assert boulder_2_move.coordinates.geojson == new_position


def test_boulder_api_edit(logged_in_client, colors, boulder):
    boulder_creator = UserFactory()
    client, user = logged_in_client
    boulder_2_update = boulder(created_by=boulder_creator)
    new_color_id = 5
    new_grade_id = 3
    data = {'color': new_color_id, 'grade': new_grade_id}
    # when
    # noinspection DuplicatedCode
    response = client.patch(
        BoulderAPI().reverse_action(
            'detail', args=[boulder_2_update.gym.pk, boulder_2_update.pk]),
        data=data, format='json')
    # then
    assert response.status_code == HTTP_200_OK
    boulder_2_update.refresh_from_db()
    assert boulder_2_update.modified_by == user
    assert boulder_2_update.grade.pk == new_grade_id
    assert boulder_2_update.color.pk == new_color_id


def test_ascent_api_post_new_ascent(logged_in_client, colors, boulder,
                                    ascent):
    """Test that post method creates new ascents"""
    # Given
    client, user = logged_in_client

    ascent_boulder = boulder()
    ascent_stub = ascent.build(boulder=ascent_boulder)

    # When
    response = client.post(
        AscentAPI().reverse_action(
            'list', args=[ascent_boulder.gym.pk, ascent_boulder.pk]
        ),
        data={'result': ascent_stub.result}, format='json'
    )

    # Then
    assert response.status_code == HTTP_201_CREATED
    ascent = Ascent.objects.first()
    assert ascent.created_by == user
    assert ascent.result == ascent_stub.result
    assert ascent.boulder == ascent_boulder


def test_ascent_api_post_existing_ascent(logged_in_client, colors, ascent):
    """
    Test that post method sets existing ascents inactive when posting to
    the same boulder for the same user
    """
    # Given
    client, user = logged_in_client

    existing_ascent = ascent(result=Ascent.PROJECT, created_by=user)

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


def test_gym_map_resources_api_get(colors, logged_in_client, gym, boulder,
                                   ascent, grade):
    client, user = logged_in_client
    incorrect_user = UserFactory()

    correct_gym = gym(created_by=user)
    incorrect_gym = gym()
    undefined_grade = grade(gym=correct_gym, grade=None)
    inactive_grade = grade(gym=correct_gym, grade=4, is_active=False)

    correct_boulders_without_ascent = boulder.create_batch(3, gym=correct_gym)

    boulders_in_other_gym = boulder.create_batch(3, gym=incorrect_gym)
    inactive_boulder = boulder(gym=correct_gym, is_active=False)

    correct_ascents = ascent.create_batch(
        3, boulder__gym=correct_gym, created_by=user
    )
    correct_boulders = [a.boulder for a in correct_ascents]

    for b in correct_boulders:
        ascent(created_by=user, boulder=b, is_active=False)

    for b in correct_boulders:
        ascent(created_by=incorrect_user, boulder=b)

    response = client.get(f'{GymMapResourcesAPI().reverse_action("list")}?'
                          f'{urlencode({"name": correct_gym.name})}')
    # then
    assert response.status_code == HTTP_200_OK
    # verify gym
    response_data = response.data.serializer.instance
    assert response_data['gym'] == correct_gym
    response_gym_data = response.data['gym']
    assert response_gym_data['created_by'] == user.pk
    response_grade_set = response_gym_data['grade_set']
    assert response_grade_set[-1]['grade'] == 'undefined'
    assert grade_2_dict(inactive_grade) not in response_grade_set
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
