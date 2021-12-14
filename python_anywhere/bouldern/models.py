"""Database models of bouldern app"""
from colorfield.fields import ColorField
from django.contrib.gis.db.models import PointField
from django.db.models import Model, CharField, ImageField, ForeignKey, \
    SET_NULL, PositiveSmallIntegerField, DateTimeField

from python_anywhere.registration.models import User


class UGC(Model):
    created_at = DateTimeField(auto_now_add=True)
    created_by = ForeignKey(User, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True


class Color(UGC):
    """Color of holds or difficulty levels"""
    name = CharField(max_length=128, unique=True)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Gym(UGC):
    """A bouldering gym"""
    name = CharField(max_length=128, unique=True)
    map = ImageField(max_length=256, upload_to='bouldern/gym_maps/')

    def __str__(self):
        return self.name


class DifficultyLevel(UGC):
    """A difficulty level in a gym"""
    level = PositiveSmallIntegerField()
    color = ForeignKey(Color, on_delete=SET_NULL, null=True)
    gym = ForeignKey(Gym, on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.level


class Boulder(UGC):
    """A boulder in a gym"""
    coordinates = PointField()
    gym = ForeignKey(Gym, on_delete=SET_NULL, null=True)

# todo: set created_by in reset_db
# todo: find other places where content is created and set created_by there
