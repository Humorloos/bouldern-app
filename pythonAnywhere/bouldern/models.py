from django.contrib.gis.db.models import PointField
from django.db import models


class Gym(models.Model):
    name = models.CharField(max_length=128)
    form_id = models.CharField(max_length=44)
    sheet_id = models.CharField(max_length=44)
    sheet_gid = models.CharField(max_length=10)
    font_size = models.IntegerField()
    gym_plan = models.ImageField(max_length=256)

    def __str__(self):
        return self.name


class SectionBoundaries(models.Model):
    x_from = models.FloatField()
    x_to = models.FloatField()
    y_from = models.FloatField()
    y_to = models.FloatField()


class Section(models.Model):
    name = models.CharField(max_length=100)
    gym = models.ForeignKey(Gym, null=True, on_delete=models.SET_NULL)
    boundaries = models.ForeignKey(SectionBoundaries, null=True,
                                   on_delete=models.SET_NULL)


class Wall(models.Model):
    position = PointField()
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)


class Boulder(models.Model):
    coordinates = PointField()
