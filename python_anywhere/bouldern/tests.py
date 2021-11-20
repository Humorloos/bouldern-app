from django.test import TestCase
from django.urls import reverse
from factory import Faker, Iterator
from factory.django import DjangoModelFactory, ImageField

from python_anywhere.bouldern.models import Gym, DifficultyLevel, Color
from python_anywhere.bouldern.views import AddGym
from settings import BASE_DIR


class GymFactory(DjangoModelFactory):
    class Meta:
        model = Gym

    name = Faker('company')
    map = ImageField(from_path=BASE_DIR / 'resources' / 'generic_gym.png')


class ColorFactory(DjangoModelFactory):
    class Meta:
        model = Color

    name = Faker('first_name')
    color = Faker('color')


class DifficultyLevelFactory(DjangoModelFactory):
    class Meta:
        model = DifficultyLevel

    level = 0
    color = Iterator(Color.objects.all())


class GymFormTest(TestCase):
    def test_post(self):
        # Given
        n_difficulty_levels = 3
        difficulty_level_range = range(n_difficulty_levels)

        colors = [ColorFactory() for _ in difficulty_level_range]

        difficulty_level_prefix = "difficultylevel_set-"
        payload = {f'{difficulty_level_prefix}TOTAL_FORMS': '3',
                   f'{difficulty_level_prefix}INITIAL_FORMS': '0'}
        payload.update(
            {f'{difficulty_level_prefix}{i}-{field}': n_difficulty_levels - i
             for field in ['color', 'level'] for i in difficulty_level_range})
        payload.update(GymFactory.stub().__dict__)

        # When
        self.client.post(reverse(AddGym.name), data=payload)

        # Then
        gym = Gym.objects.first()
        self.assert_correct_gym(gym, payload)

        difficulty_levels = DifficultyLevel.objects.all()
        self.assertEqual(len(difficulty_levels), n_difficulty_levels)
        for difficulty_level in difficulty_levels:
            self.assert_correct_gym(difficulty_level.gym, payload)
            self.assertIn(difficulty_level.color, colors)
            self.assertIn(difficulty_level.level - 1, difficulty_level_range)

    def assert_correct_gym(self, gym, payload):
        self.assertEqual(gym.name, payload['name'])
        self.assertEqual(gym.map.size, payload['map'].size)
