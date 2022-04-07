"""Database models of bouldern app"""
from colorfield.fields import ColorField
from django.contrib.gis.db.models import PointField
from django.db.models import Model, CharField, ImageField, ForeignKey, \
    SET_NULL, PositiveSmallIntegerField, DateTimeField, PROTECT, BooleanField
from django.utils import timezone
from simple_history.models import HistoricalRecords

from python_anywhere.accounts.models import User


class UGC(Model):
    """Abstract model for user-generated content"""
    created_at = DateTimeField(auto_now_add=True)
    created_by = ForeignKey(
        User, on_delete=SET_NULL, null=True, related_name='created_%(class)ss',
        related_query_name='created_%(class)s')
    modified_at = DateTimeField(auto_now=True)
    modified_by = ForeignKey(
        User, on_delete=SET_NULL, null=True, related_name='modified_%(class)ss',
        related_query_name='modified_%(class)s')
    is_active = BooleanField(default=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class Color(UGC):
    """Color of holds or grades"""
    name = CharField(max_length=128, unique=True)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Gym(UGC):
    """A bouldering gym"""
    name = CharField(max_length=128, unique=True)
    map = ImageField(max_length=256, upload_to='bouldern/gym_maps/', null=True)

    def __str__(self):
        return self.name


class Grade(UGC):
    """A grade in a gym"""
    grade = PositiveSmallIntegerField(null=True)
    color = ForeignKey(Color, on_delete=SET_NULL, null=True)
    gym = ForeignKey(Gym, on_delete=SET_NULL, null=True)

    def __str__(self):
        return str(self.grade)


class Boulder(UGC):
    """A boulder in a gym"""
    coordinates = PointField()
    gym = ForeignKey(Gym, on_delete=SET_NULL, null=True)
    grade = ForeignKey(Grade, on_delete=PROTECT, null=True)
    color = ForeignKey(Color, on_delete=PROTECT, null=True)

    @property
    def age(self):
        """The boulder's age in days"""
        return (timezone.now() - self.created_at).days


class Ascent(UGC):
    """An attempt to ascent a boulder"""

    PROJECT = 0
    TOP = 1
    FLASH = 2

    RESULT_CHOICES = ((PROJECT, ''), (TOP, ''), (FLASH, ''))

    result = PositiveSmallIntegerField(choices=RESULT_CHOICES)
    boulder = ForeignKey(Boulder, on_delete=PROTECT)


class FavoriteGym(UGC):
    """An entry in a user's collection of favorite gyms"""

    gym = ForeignKey(Gym, on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.gym.name
