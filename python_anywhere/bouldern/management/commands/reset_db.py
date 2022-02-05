"""Custom django command for resetting database to default state"""

from subprocess import call

from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from factory.django import ImageField

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.factories import ColorFactory, GymFactory, \
    BoulderFactory, AscentFactory
from python_anywhere.bouldern.tests.conftest import default_colors
from python_anywhere.settings import BASE_DIR, env, RESOURCES_DIR


class Command(BaseCommand):
    """Command for resetting database to default state"""
    help = 'Resets database to default state'

    def handle(self, *args, **options):
        manage_args = ['python', 'manage.py']
        call(manage_args + ['flush', '--no-input'], cwd=BASE_DIR)

        # create super user
        UserFactory(email=env('ADMIN_EMAIL'),
                    username='admin',
                    password=env('ADMIN_PASSWORD'),
                    is_superuser=True,
                    is_staff=True, )

        # create test user
        UserFactory(email='wetBonez@web.de',
                    username='wetBonez',
                    password='youcantknowthispassword123')

        # add default colors
        for name, color in default_colors.items():
            ColorFactory(name=name, color=color)

        # add generic gym
        generic_gym = GymFactory(
            name='Generic Gym',
            map=ImageField(from_path=RESOURCES_DIR / 'generic_gym.png'))

        # add boulders
        boulder = BoulderFactory(
            gym=generic_gym,
            coordinates=Point(799, 645),
            grade=generic_gym.grade_set.first()
        )
        BoulderFactory(gym=generic_gym, coordinates=Point(1041, 716))

        # add ascent
        AscentFactory(boulder=boulder)

        # add green gym
        GymFactory(
            name='Green Gym',
            map=ImageField(from_path=RESOURCES_DIR / 'green_gym.png'))
