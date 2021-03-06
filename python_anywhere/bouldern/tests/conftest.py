import pytest

default_colors = {
    'Yellow': '#f6c026',
    'Red': '#d60000',
    'Green': '#0b8043',
    'Blue': '#039be5',
    'Orange': '#f5511d',
    'Purple': '#8e24aa',
    'White': '#eeede9',
    'Black': '#000000',
    'Grey': '#848284',
}


@pytest.fixture
def colors(db):
    from python_anywhere.bouldern.factories import ColorFactory
    yield [ColorFactory(name=name, color=color) for name, color in
           default_colors.items()]


@pytest.fixture
def favorite_gym():
    from python_anywhere.bouldern.factories import FavoriteGymFactory
    yield FavoriteGymFactory


@pytest.fixture
def gym():
    from python_anywhere.bouldern.factories import GymFactory
    yield GymFactory


@pytest.fixture
def boulder():
    from python_anywhere.bouldern.factories import BoulderFactory
    yield BoulderFactory


@pytest.fixture
def ascent():
    from python_anywhere.bouldern.factories import AscentFactory
    yield AscentFactory


@pytest.fixture
def grade():
    from python_anywhere.bouldern.factories import GradeFactory
    yield GradeFactory
