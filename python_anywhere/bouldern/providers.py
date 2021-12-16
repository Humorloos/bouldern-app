"""Custom providers for faker"""
from django.contrib.gis.geos import Point
from faker.providers.geo import Provider


class GeoProvider(Provider):
    """Provider of geographic data"""
    def point(self):
        """
        Provides a point in geojson format with random latitude and longitude
        :return: the point in geojson format
        """
        return Point(self.latlng()).geojson
