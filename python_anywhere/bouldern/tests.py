"""Tests for bouldern app"""
from django.test import TestCase
from django.urls import reverse

from python_anywhere.bouldern.factories import ColorFactory, GymFactory
from python_anywhere.bouldern.models import Gym, DifficultyLevel
from python_anywhere.bouldern.views import AddGym
from python_anywhere.registration.factories import UserFactory


class AddGymTest(TestCase):
    """Test class for AddGym view"""

    def test_post(self):
        """Test that post method works correctly"""
        # Given
        # login
        password = 'OAwIYQRCdiplaCIwEEcn'
        user = UserFactory(password=password)
        self.client.login(username=user.email, password=password)

        n_difficulty_levels = 3
        difficulty_level_range = range(n_difficulty_levels)

        colors = [ColorFactory() for _ in difficulty_level_range]

        difficulty_level_prefix = "difficultylevel_set-"
        payload = {f'{difficulty_level_prefix}TOTAL_FORMS': '3',
                   f'{difficulty_level_prefix}INITIAL_FORMS': '0'}
        payload.update(
            {f'{difficulty_level_prefix}{i}-{field}': n_difficulty_levels - i
             for field in ['color', 'level'] for i in difficulty_level_range})
        payload.update({key: GymFactory.stub().__dict__[key]
                        for key in ['map', 'name']})

        # When
        self.client.post(reverse(AddGym.name), data=payload)

        # Then
        gym = Gym.objects.first()
        self.assert_correct_gym(gym, payload, user)

        difficulty_levels = DifficultyLevel.objects.all()
        self.assertEqual(len(difficulty_levels), n_difficulty_levels)
        for difficulty_level in difficulty_levels:
            self.assert_correct_gym(difficulty_level.gym, payload, user)
            self.assertIn(difficulty_level.color, colors)
            self.assertIn(difficulty_level.level - 1, difficulty_level_range)
            self.assertEqual(difficulty_level.created_by, user)

    def assert_correct_gym(self, gym, payload, user):
        """
        Assert that provided gym is equal to gym described in payload
        :param gym: gym to compare
        :param payload: payload from post request containing gym specifications
        :param user: user the gym is supposed to have been created by
        """
        self.assertEqual(gym.name, payload['name'])
        self.assertEqual(gym.map.size, payload['map'].size)
        self.assertEqual(gym.created_by, user)
