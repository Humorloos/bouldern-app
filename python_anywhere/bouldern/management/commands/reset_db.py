"""Custom django command for resetting database to default state"""

import os
import re
from subprocess import call

from django.core.management import BaseCommand
from factory.django import ImageField

from python_anywhere.bouldern.factories import ColorFactory, GymFactory, DifficultyLevelFactory
from python_anywhere.bouldern.management.commands._default_colors import default_colors
from python_anywhere.registration.factories import UserFactory
from python_anywhere.settings import DATABASES, BASE_DIR, PROJECT_DIR, env


class Command(BaseCommand):
    """Command for resetting database to default state"""
    help = 'Resets database to default state'

    def handle(self, *args, **options):
        if os.path.exists(DATABASES['default']['NAME']):
            os.remove(DATABASES['default']['NAME'])

        for app in ['bouldern', 'registration']:
            migrations_dir = PROJECT_DIR / app / 'migrations'
            for filename in os.listdir(migrations_dir):
                if re.search(r'^\d{4}_.*\.py$', filename) is not None:
                    os.remove(migrations_dir / filename)

        manage_args = ['python', 'manage.py']
        call(manage_args + ['makemigrations'], cwd=BASE_DIR)
        call(manage_args + ['migrate'], cwd=BASE_DIR)

        # create super user
        UserFactory(email=env('ADMIN_EMAIL'),
                    username='admin',
                    password=env('ADMIN_PASSWORD'),
                    is_superuser=True,
                    is_staff=True, )

        # add default colors
        colors = [ColorFactory(name=name, color=color) for name, color in default_colors.items()]

        # add generic gym
        generic_gym = GymFactory(name='generic_gym',
                                 map=ImageField(from_path=BASE_DIR / 'resources' / 'generic_gym.png'))

        # add difficulty levels for generic gym
        for level, color in enumerate(colors[:7]):
            DifficultyLevelFactory(level=level, color=color, gym=generic_gym)
