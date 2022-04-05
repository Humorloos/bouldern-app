"""Custom django command for generating test db resources"""
from django.core.management import BaseCommand
import pandas as pd

from python_anywhere.bouldern.models import Boulder
from python_anywhere.settings import RESOURCES_DIR


class Command(BaseCommand):
    """Command for generating test db resources"""
    help = 'Generates test db resources from current database contents'

    def handle(self, *args, **options):
        active_boulders = Boulder.objects.filter(is_active=True)
        pd.DataFrame({
                         'id': boulder.pk,
                         'grade': boulder.grade.pk,
                         'color': boulder.color.pk,
                         'coordinates': boulder.coordinates.geojson,
                     } for boulder in active_boulders) \
            .to_csv(RESOURCES_DIR / 'boulders.csv', index=False)

        pd.DataFrame({
                         'id': ascent.pk,
                         'boulder': ascent.boulder.pk,
                         'result': ascent.result,
                     } for ascent in [
                         boulder.ascent_set.filter(is_active=True).first()
                         for boulder in active_boulders if
                         boulder.ascent_set.first()]) \
            .to_csv(RESOURCES_DIR / 'ascents.csv', index=False)
