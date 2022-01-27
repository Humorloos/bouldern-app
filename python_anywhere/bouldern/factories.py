"""
This script contains factories for building model instances of the bouldern app
"""

from random import choice

from factory import Iterator, Faker, LazyAttribute, RelatedFactoryList, \
    SubFactory
from factory.django import DjangoModelFactory, ImageField

from python_anywhere.accounts.models import User
from python_anywhere.bouldern.models import Color, Gym, DifficultyLevel, UGC, \
    Boulder
from python_anywhere.bouldern.providers import GeoProvider
from python_anywhere.settings import RESOURCES_DIR

Faker.add_provider(GeoProvider)


class UGCFactory(DjangoModelFactory):
    """Abstract factory, serves as superclass for all UGC subclasses"""
    class Meta:
        model = UGC
        abstract = True

    created_by = User.objects.first()
    modified_by = User.objects.first()


class ColorFactory(UGCFactory):
    """Factory for building color instances"""

    class Meta:
        model = Color

    name = Faker('color_name')
    color = Faker('color')


class DifficultyLevelFactory(UGCFactory):
    """Factory for building difficulty level instances"""

    class Meta:
        model = DifficultyLevel

    level = LazyAttribute(lambda o: o.gym.difficultylevel_set.count() + 1)
    color = Iterator(Color.objects.all())
    gym = Gym.objects.first()


class GymFactory(UGCFactory):
    """Factory for building gym instances"""

    class Meta:
        model = Gym

    name = Faker('company')
    map = ImageField(from_path=RESOURCES_DIR / 'generic_gym.png')
    difficulty_levels = RelatedFactoryList(
        DifficultyLevelFactory,
        factory_related_name='gym',
        size=7
    )


class BoulderFactory(UGCFactory):
    """Factory for building boulders"""

    class Meta:
        model = Boulder

    coordinates = Faker('point')
    gym = SubFactory(GymFactory)
    # set random difficulty from the boulder's gym
    difficulty = LazyAttribute(
        lambda o: DifficultyLevel.objects.get(pk=choice(
            DifficultyLevel.objects.filter(gym=o.gym).values_list('pk'))[0]))
    # default color is difficultylevel's color
    color = LazyAttribute(lambda o: o.difficulty.color)
