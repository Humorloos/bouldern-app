from django.contrib.gis.geos import Point
from faker.providers.geo import Provider


class GeoProvider(Provider):
    def point(self):
        return Point(self.latlng()).geojson
