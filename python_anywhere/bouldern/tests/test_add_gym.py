from django.urls import reverse
from faker import Faker

from python_anywhere.bouldern.models import Gym, DifficultyLevel
from python_anywhere.bouldern.views import AddGym, AddGymRest
from python_anywhere.accounts.factories import UserFactory


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
    colors = [ColorFactory() for _ in difficulty_level_range]

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


def test_add_gym_rest(logged_in_client):
    """Test that post method works correctly"""
    # Given
    from python_anywhere.bouldern.factories import GymFactory
    payload = {key: GymFactory.stub().__dict__[key]
               for key in ['map', 'name']}
    client, user = logged_in_client

    # When
    client.post(reverse(AddGymRest.name), data=payload, format='multipart')

    # Then
    gym = Gym.objects.first()
    assert_correct_gym(gym, payload, user)
