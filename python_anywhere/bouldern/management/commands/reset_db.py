"""Custom django command for resetting database to default state"""
from datetime import timedelta
from subprocess import call
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from django.utils import timezone
from factory.django import ImageField

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.factories import ColorFactory, GymFactory, \
    BoulderFactory, AscentFactory, FavoriteGymFactory, GradeFactory
from python_anywhere.bouldern.models import Color
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
        test_user = UserFactory(email='wetbonez@web.de',
                                username='wetBonez',
                                password='youcantknowthispassword123')

        # add default colors
        for name, color in default_colors.items():
            ColorFactory(name=name, color=color)

        # add generic gym
        generic_gym = GymFactory(
            name='Generic Gym',
            map=ImageField(from_path=RESOURCES_DIR / 'generic_gym.png'))

        # add undefined grade
        GradeFactory(gym=generic_gym, grade=None,
                     color=Color.objects.filter(name='Grey').first())

        # add boulders
        boulder = BoulderFactory(
            gym=generic_gym,
            coordinates=Point(799, 645),
            grade=generic_gym.grade_set.first()
        )
        boulder.created_at = timezone.now() - timedelta(days=15)
        boulder.save()
        BoulderFactory(
            gym=generic_gym,
            coordinates=Point(1041, 716),
            grade=generic_gym.grade_set.all()[1]
        )

        # add ascent
        AscentFactory(boulder=boulder)

        # add green gym
        GymFactory(
            name='Green Gym',
            map=ImageField(from_path=RESOURCES_DIR / 'green_gym.png'))

        # add favorite gym
        FavoriteGymFactory(gym=generic_gym)
        FavoriteGymFactory(created_by=test_user, gym=generic_gym)
