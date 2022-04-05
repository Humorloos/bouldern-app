"""Custom django command for resetting database to default state"""
from datetime import timedelta
from subprocess import call

import pandas as pd

from django.core.management import BaseCommand
from django.utils import timezone
from factory.django import ImageField
from rest_framework_gis.fields import GeometryField

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.factories import ColorFactory, GymFactory, \
    BoulderFactory, AscentFactory, FavoriteGymFactory, GradeFactory
from python_anywhere.bouldern.models import Color, Grade, Boulder
from python_anywhere.bouldern.tests.conftest import default_colors
from python_anywhere.settings import BASE_DIR, RESOURCES_DIR


class Command(BaseCommand):
    """Command for resetting database to default state"""
    help = 'Resets database to default state'

    def handle(self, *args, **options):
        manage_args = ['python', 'manage.py']
        call(manage_args + ['flush', '--no-input'], cwd=BASE_DIR)

        # create super user
        UserFactory(email='admin@boulderholder.com',
                    username='admin',
                    password='admin',
                    is_superuser=True,
                    is_staff=True, )
        # create test user
        test_user = UserFactory(email='testUser@web.de',
                                username='myUsername',
                                password='youcantknowthispassword123')

        # add default colors
        for name, color in default_colors.items():
            ColorFactory(name=name, color=color)

        # add generic gym
        generic_gym = GymFactory(
            name='Generic Gym',
            map=ImageField(from_path=RESOURCES_DIR / 'generic_gym.png'))

        # add green gym
        GymFactory(
            name='Green Gym',
            map=ImageField(from_path=RESOURCES_DIR / 'green_gym.png'))

        # add undefined grade
        GradeFactory(gym=generic_gym, grade=None,
                     color=Color.objects.filter(name='Grey').first())

        # add boulders
        boulder_data = pd.read_csv(RESOURCES_DIR / 'boulders.csv')
        geometry_field = GeometryField()
        boulders = [BoulderFactory(
            id=boulder.id,
            gym=generic_gym,
            coordinates=geometry_field.to_internal_value(boulder.coordinates),
            grade=Grade.objects.get(pk=boulder.grade),
            color=Color.objects.get(pk=boulder.color),
        ) for _, boulder in boulder_data.iterrows()]
        older_boulder = boulders[0]
        older_boulder.created_at = timezone.now() - timedelta(days=15)
        older_boulder.save()

        # add ascents
        ascent_data = pd.read_csv(RESOURCES_DIR / 'ascents.csv')
        for _, ascent in ascent_data.iterrows():
            AscentFactory(
                id=ascent.id,
                boulder=Boulder.objects.get(pk=ascent.boulder),
                result=ascent.result,
                created_by=test_user,
            )

        # add favorite gym
        FavoriteGymFactory(gym=generic_gym)
        FavoriteGymFactory(created_by=test_user, gym=generic_gym)
