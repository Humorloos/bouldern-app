"""This script contains factories for building model instances of the bouldern app"""

from factory import Faker, Iterator
from factory.django import DjangoModelFactory, ImageField

from python_anywhere.bouldern.models import Color, Gym, DifficultyLevel
from python_anywhere.settings import BASE_DIR


class ColorFactory(DjangoModelFactory):
    """Factory for building color instances"""

    class Meta:
        model = Color

    name = Faker('first_name')
    color = Faker('color')


class GymFactory(DjangoModelFactory):
    """Factory for building gym instances"""

    class Meta:
        model = Gym

    name = Faker('company')
    map = ImageField(from_path=BASE_DIR / 'resources' / 'generic_gym.png')


class DifficultyLevelFactory(DjangoModelFactory):
    """Factory for building difficulty level instances"""

    class Meta:
        model = DifficultyLevel

    level = 0
    color = Iterator(Color.objects.all())
    gym = Iterator(Color.objects.all())
