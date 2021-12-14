"""
This script contains factories for building model instances of the bouldern app
"""

from factory import Faker, Iterator
from factory.django import DjangoModelFactory, ImageField

from python_anywhere.bouldern.models import Color, Gym, DifficultyLevel, UGC
from python_anywhere.registration.models import User
from python_anywhere.settings import RESOURCES_DIR


class UGCFactory(DjangoModelFactory):
    class Meta:
        model = UGC
        abstract = True

    created_by = User.objects.get(pk=1)


class ColorFactory(UGCFactory):
    """Factory for building color instances"""

    class Meta:
        model = Color

    name = Faker('first_name')
    color = Faker('color')


class GymFactory(UGCFactory):
    """Factory for building gym instances"""

    class Meta:
        model = Gym

    name = Faker('company')
    map = ImageField(from_path=RESOURCES_DIR / 'generic_gym.png')


class DifficultyLevelFactory(UGCFactory):
    """Factory for building difficulty level instances"""

    class Meta:
        model = DifficultyLevel

    level = 0
    color = Iterator(Color.objects.all())
    gym = Iterator(Color.objects.all())
