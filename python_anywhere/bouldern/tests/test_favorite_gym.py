from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_200_OK

from python_anywhere.accounts.factories import UserFactory
from python_anywhere.bouldern.models import FavoriteGym
from python_anywhere.bouldern.views import FavoriteGymAPI


def test_add_favorite_gym(logged_in_client, colors, gym, favorite_gym):
    # given
    target_gym = gym()
    new_favorite_gym = favorite_gym.build(gym=target_gym)

    payload = {'gym': new_favorite_gym.gym.name}

    client, user = logged_in_client

    # when
    response = client.post(FavoriteGymAPI().reverse_action('list'),
                           data=payload, format='json')

    # then
    assert response.status_code == HTTP_201_CREATED
    created_favorite = response.data.serializer.instance
    assert created_favorite.gym == target_gym
    assert created_favorite.created_by == user


def test_remove_favorite_gym(logged_in_client, favorite_gym, colors):
    # given
    client, user = logged_in_client
    favorite_gym_2_remove = favorite_gym(created_by=user)

    # when
    response = client.delete(
        FavoriteGymAPI().reverse_action('detail', args=[favorite_gym_2_remove.gym.name]))

    # then
    assert response.status_code == HTTP_204_NO_CONTENT
    deleted_favorite = FavoriteGym.objects.get(pk=favorite_gym_2_remove.pk)
    assert not deleted_favorite.is_active


def test_get_favorite_gyms(logged_in_client, favorite_gym, colors):
    # given
    client, user = logged_in_client

    favorite_gyms = favorite_gym.create_batch(5, created_by=user)
    old_favorites = favorite_gym.create_batch(
        2, created_by=user, is_active=False)
    other_user = UserFactory()
    favorites_by_other_user = favorite_gym.create_batch(
        2, created_by=other_user)

    # when
    response = client.get(FavoriteGymAPI().reverse_action('list'))

    # then
    assert response.status_code == HTTP_200_OK
    returned_favorites = response.data.serializer.instance
    assert all(g in returned_favorites for g in favorite_gyms)
    assert not any(g in returned_favorites for g in old_favorites)
    assert not any(g in returned_favorites for g in favorites_by_other_user)
