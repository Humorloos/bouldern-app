from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.accounts.models import User


def test_add_gym_rest(db):
    """Test that post method works correctly"""
    # Given
    client = APIClient()
    password = Faker().password()
    user = UserFactory.build(password=password)
    payload = {key: user.__dict__[key] for key in ['username', 'email']}
    payload.update({f'password{i}': password for i in range(1, 3)})

    # When
    client.post(reverse('rest_register'), data=payload,
                format='json')

    # Then
    created_user = User.objects.first()
    assert created_user.email == payload['email']
    assert created_user.username == payload['username']
    assert created_user.check_password(password)
