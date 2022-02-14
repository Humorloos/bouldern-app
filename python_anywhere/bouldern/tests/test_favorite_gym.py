from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from python_anywhere.bouldern.models import FavoriteGym
from python_anywhere.bouldern.views import FavoriteGymAPI


def test_add_favorite_gym(logged_in_client_rest, colors):
    # given
    from python_anywhere.bouldern.factories import GymFactory
    gym = GymFactory()
    from python_anywhere.bouldern.factories import FavoriteGymFactory
    favorite_gym = FavoriteGymFactory.build(gym=gym)

    payload = {'gym': favorite_gym.gym.name}

    client, user = logged_in_client_rest

    # when
    response = client.post(FavoriteGymAPI().reverse_action('list'),
                           data=payload, format='json')

    # then
    assert response.status_code == HTTP_201_CREATED
    created_favorite = response.data.serializer.instance
    assert created_favorite.gym == gym
    assert created_favorite.created_by == user


def test_remove_favorite_gym(logged_in_client_rest, colors):
    # given
    from python_anywhere.bouldern.factories import FavoriteGymFactory
    favorite_gym = FavoriteGymFactory()

    client, user = logged_in_client_rest

    # when
    response = client.delete(
        FavoriteGymAPI().reverse_action('detail', args=[favorite_gym.gym.name]))

    # then
    assert response.status_code == HTTP_204_NO_CONTENT
    deleted_favorite = FavoriteGym.objects.get(pk=favorite_gym.pk)
    assert not deleted_favorite.is_active
