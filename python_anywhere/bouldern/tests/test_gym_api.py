from collections import OrderedDict

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from python_anywhere.bouldern.models import Gym, Grade, Color
from python_anywhere.bouldern.serializers import GradeSerializer
from python_anywhere.bouldern.views import GymAPI


def assert_correct_gym(gym, payload, user):
    """
    Assert that provided gym is equal to gym described in payload
    :param gym: gym to compare
    :param payload: payload from post request containing gym specifications
    :param user: user the gym is supposed to have been created by
    """
    assert gym.name == payload['name']
    assert gym.map.size == payload['map'].size
    assert gym.created_by == user


def test_create_gym(logged_in_client_rest, colors):
    """Test that post method works correctly"""
    # Given
    from python_anywhere.bouldern.factories import GymFactory
    gym_stub = GymFactory.build()
    client, user = logged_in_client_rest
    n_grades = 3
    grade_range = range(1, n_grades + 1)
    from python_anywhere.bouldern.factories import GradeFactory
    grade_stubs = [
        GradeFactory.stub(gym=gym_stub, grade=i)
        for i in grade_range]
    grade_stubs += [GradeFactory.stub(gym=gym_stub, grade='undefined')]
    json_payload = {
        'name': gym_stub.name,
        'grade_set': [{
            'color': grade.color.pk,
            'grade': grade.grade
        } for grade in grade_stubs]
    }

    # When
    response = client.post(GymAPI().reverse_action('list'),
                           data=json_payload, format='json')
    # Then
    assert response.status_code == HTTP_201_CREATED
    gym = Gym.objects.first()
    assert gym.name == gym_stub.name
    grades = list(Grade.objects.all())
    assert len(grades) == n_grades + 1
    for grade in grades[:-1]:
        assert grade.gym.name == gym_stub.name
        assert grade.color in colors
        assert grade.grade in grade_range
        assert grade.created_by == user
    assert grades[-1].grade is None
    # When
    multipart_payload = {'map': gym_stub.map}
    client.patch(
        GymAPI().reverse_action('detail', args=[response.data['id']]),
        data=multipart_payload, format='multipart')
    # Then
    gym = Gym.objects.first()
    assert_correct_gym(gym, json_payload | multipart_payload, user)


def grade_2_dict(grade):
    return OrderedDict(GradeSerializer(grade).data)


def test_update_gym_grades(logged_in_client_rest, colors):
    # Given
    from python_anywhere.accounts.factories import UserFactory
    gym_author = UserFactory()
    from python_anywhere.bouldern.factories import GymFactory
    gym = GymFactory(created_by=gym_author, modified_by=gym_author)

    # unchanged grades
    grades = list(gym.grade_set.all())

    # removed grades
    removed_grades = [grades.pop() for _ in range(2)]

    # updated grade
    updated_grade = grades[-1]
    updated_grade.color = colors[0]
    grade_payload = [
        {'grade': grade.grade, 'color': grade.color.pk, 'id': grade.pk} for
        grade in grades]

    # new grade
    new_grade_grade = len(grades) + 1

    # new undefined grade
    grade_payload += [{'grade': new_grade_grade, 'color': 3}]

    grade_payload += [{'grade': 'undefined', 'color': 5}]

    client, user = logged_in_client_rest

    # When
    response = client.patch(
        GymAPI().reverse_action('detail', args=[gym.pk]),
        data={'grade_set': grade_payload}, format='json')

    # Then
    assert response.status_code == HTTP_200_OK
    modified_grade_set = response.data['grade_set']
    assert not any(grade_2_dict(grade) in modified_grade_set
                   for grade in removed_grades)
    assert all(grade_2_dict(grade) in modified_grade_set for grade in grades)
    assert any(grade['grade'] == new_grade_grade
               for grade in modified_grade_set)
    assert any(grade['grade'] == 'undefined' for grade in modified_grade_set)
    assert next(grade for grade in modified_grade_set
                if grade['id'] == updated_grade.pk)['color'] == \
           updated_grade.color.pk
    for grade in grades:
        grade.refresh_from_db()
    assert all(grade.modified_by == gym_author for grade in grades[:-1])
    assert updated_grade.modified_by == user

