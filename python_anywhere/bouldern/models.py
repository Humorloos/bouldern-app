"""Database models of bouldern app"""
from django.contrib.gis.db.models import PointField
from django.db.models import Model, CharField, ImageField, ForeignKey, SET_NULL


class Gym(Model):
    name = CharField(max_length=128)
    map = ImageField(max_length=256, upload_to='bouldern/gym_maps/')

    def __str__(self):
        return self.name


class Boulder(Model):
    """A boulder in a gym"""
    coordinates = PointField()
    gym = ForeignKey(Gym, on_delete=SET_NULL, null=True)
