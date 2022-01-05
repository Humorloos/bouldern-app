import json

from django.utils.http import urlencode
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.models import Gym, DifficultyLevel
from python_anywhere.bouldern.serializers import BoulderSerializer
from python_anywhere.bouldern.views import AddGym, GymAPI


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


def test_add_gym(client, db):
    """Test that post method works correctly"""
    # Given
    # login
    password = Faker().password()
    user = UserFactory(password=password)
    client.login(username=user.email, password=password)

    n_difficulty_levels = 3
    difficulty_level_range = range(n_difficulty_levels)

    from python_anywhere.bouldern.factories import ColorFactory
    faker = Faker()
    colors = [ColorFactory(name=faker.unique.color())
              for _ in difficulty_level_range]

    difficulty_level_prefix = "difficultylevel_set-"
    payload = {
        f'{difficulty_level_prefix}TOTAL_FORMS': str(n_difficulty_levels),
        f'{difficulty_level_prefix}INITIAL_FORMS': '0'}
    payload.update(
        {f'{difficulty_level_prefix}{i}-{field}': n_difficulty_levels - i
         for field in ['color', 'level'] for i in difficulty_level_range})

    from python_anywhere.bouldern.factories import GymFactory
    payload.update({key: GymFactory.stub().__dict__[key]
                    for key in ['map', 'name']})

    # When
    response = client.post(reverse(AddGym.name), data=payload)

    # Then
    gym = Gym.objects.first()
    assert_correct_gym(gym, payload, user)

    difficulty_levels = DifficultyLevel.objects.all()
    assert len(difficulty_levels) == n_difficulty_levels
    for difficulty_level in difficulty_levels:
        assert_correct_gym(difficulty_level.gym, payload, user)
        assert difficulty_level.color in colors
        assert difficulty_level.level - 1 in difficulty_level_range
        assert difficulty_level.created_by == user
    assert response.url == reverse('index')


def test_add_gym_rest(logged_in_client_rest):
    """Test that post method works correctly"""
    # Given
    from python_anywhere.bouldern.factories import GymFactory
    gym_stub = GymFactory.stub()
    client, user = logged_in_client_rest
    n_difficulty_levels = 3
    difficulty_level_range = range(n_difficulty_levels)
    from python_anywhere.bouldern.factories import ColorFactory
    faker = Faker()
    colors = [ColorFactory(name=faker.unique.color())
              for _ in difficulty_level_range]
    json_payload = {
        'name': gym_stub.name,
        'difficultylevel_set': [
            {field: n_difficulty_levels - i for field in ['color', 'level']}
            for i in difficulty_level_range]}

    # When
    response = client.post(GymAPI().reverse_action('list'),
                           data=json_payload, format='json')
    # Then
    assert response.status_code == HTTP_201_CREATED
    gym = Gym.objects.first()
    assert gym.name == gym_stub.name
    difficulty_levels = DifficultyLevel.objects.all()
    assert len(difficulty_levels) == n_difficulty_levels
    for difficulty_level in difficulty_levels:
        assert difficulty_level.gym.name == gym_stub.name
        assert difficulty_level.color in colors
        assert difficulty_level.level - 1 in difficulty_level_range
        assert difficulty_level.created_by == user
    # When
    multipart_payload = {'map': gym_stub.map}
    client.patch(
        GymAPI().reverse_action('detail', args=[response.data['id']]),
        data=multipart_payload, format='multipart')
    # Then
    gym = Gym.objects.first()
    assert_correct_gym(gym, json_payload | multipart_payload, user)


def test_gym_api_get(logged_in_client_rest):
    # Given
    from python_anywhere.bouldern.factories import GymFactory
    correct_gym = GymFactory(name='testName')
    GymFactory()
    from python_anywhere.bouldern.factories import BoulderFactory
    boulders = [BoulderFactory(gym=correct_gym) for _ in range(3)]
    client, user = logged_in_client_rest
    # When
    response = client.get(f'{GymAPI().reverse_action("list")}?'
                          f'{urlencode({"name": correct_gym.name})}')
    # Then
    assert response.status_code == HTTP_200_OK
    assert set(response.data.serializer.instance) == {correct_gym}
    assert json.loads(response.content)[0]['boulder_set'][0]['coordinates'] == \
           BoulderSerializer(boulders[0]).data['coordinates']
