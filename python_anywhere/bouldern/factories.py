"""
This script contains factories for building model instances of the bouldern app
"""

from random import choice
from factory import Iterator, Faker, LazyAttribute, RelatedFactoryList, \
    SubFactory, SelfAttribute
from factory.django import DjangoModelFactory, ImageField

from python_anywhere.accounts.models import User
from python_anywhere.bouldern.models import Color, Gym, Grade, UGC, \
    Boulder, Ascent, FavoriteGym
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


class GradeFactory(UGCFactory):
    """Factory for building grade instances"""

    class Meta:
        model = Grade

    grade = LazyAttribute(lambda o: o.gym.grade_set.count() + 1)
    color = Iterator(Color.objects.all())
    gym = Gym.objects.first()


class GymFactory(UGCFactory):
    """Factory for building gym instances"""

    class Meta:
        model = Gym

    name = Faker('company')
    map = ImageField(from_path=RESOURCES_DIR / 'generic_gym.png')
    grades = RelatedFactoryList(
        GradeFactory,
        factory_related_name='gym',
        size=7,
        created_by=SelfAttribute('..created_by'),
        modified_by=SelfAttribute('..modified_by')
    )


class BoulderFactory(UGCFactory):
    """Factory for building boulders"""

    class Meta:
        model = Boulder

    coordinates = Faker('point')
    gym = SubFactory(GymFactory)
    # set random grade from the boulder's gym
    grade = LazyAttribute(
        lambda o: Grade.objects.get(pk=choice(
            Grade.objects.filter(gym=o.gym).values_list('pk'))[0]))
    # default color is grade's color
    color = LazyAttribute(lambda o: o.grade.color)


class AscentFactory(UGCFactory):
    """Factory for building ascents"""

    class Meta:
        model = Ascent

    result = Ascent.TOP
    boulder = SubFactory(BoulderFactory)


class FavoriteGymFactory(UGCFactory):
    """Factory for building favorite gyms"""

    class Meta:
        model = FavoriteGym

    gym = SubFactory(GymFactory)
