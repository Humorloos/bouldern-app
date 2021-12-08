"""Database models of bouldern app"""
from colorfield.fields import ColorField
from django.contrib.gis.db.models import PointField
from django.db.models import Model, CharField, ImageField, ForeignKey, SET_NULL, \
    PositiveSmallIntegerField


# todo: define managed mixin (for now with created at and created by) for use in all user-created content: https://stackoverflow.com/a/25817237/12566791

class Color(Model):
    """Color of holds or difficulty levels"""
    name = CharField(max_length=128, unique=True)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Gym(Model):
    """A bouldering gym"""
    name = CharField(max_length=128, unique=True)
    map = ImageField(max_length=256, upload_to='bouldern/gym_maps/')

    def __str__(self):
        return self.name


class DifficultyLevel(Model):
    """A difficulty level in a gym"""
    level = PositiveSmallIntegerField()
    color = ForeignKey(Color, on_delete=SET_NULL, null=True)
    gym = ForeignKey(Gym, on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.level


class Boulder(Model):
    """A boulder in a gym"""
    coordinates = PointField()
    gym = ForeignKey(Gym, on_delete=SET_NULL, null=True)
