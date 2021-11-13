from django.contrib.gis.db.models import PointField
from django.db import models


class Boulder(models.Model):
    coordinates = PointField()
