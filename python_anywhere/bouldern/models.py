"""Database models of bouldern app"""
from django.contrib.gis.db.models import PointField
from django.db import models


class Boulder(models.Model):
    """A boulder in a gym"""
    coordinates = PointField()
