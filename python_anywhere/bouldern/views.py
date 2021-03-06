"""Module containing the views of the bouldern app"""
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, ListModelMixin, \
    UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet
from url_filter.integrations.drf import DjangoFilterBackend

from python_anywhere.bouldern.models import Boulder, Gym, Color, Ascent, \
    FavoriteGym
from python_anywhere.bouldern.serializers import GymSerializer, ColorSerializer, \
    BoulderSerializer, AscentSerializer, GymMapResourcesSerializer, \
    FavoriteGymSerializer, GymNameSerializer
from python_anywhere.views import ReversibleViewSet


class CreateUGCMixin(CreateModelMixin, GenericViewSet):
    """Mixin for creating UGC instances"""

    def perform_create(self, serializer, **kwargs):
        serializer.save(created_by=self.request.user,
                        modified_by=self.request.user,
                        **kwargs)


class DestroyUGCMixin(DestroyModelMixin, GenericViewSet):
    """Mixin for destroying UGC instances by setting them inactive"""

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.modified_by = self.request.user
        instance.save()


class ColorAPI(ReversibleViewSet, ListModelMixin, CreateUGCMixin):
    """REST API for adding colors"""
    basename = 'color'
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class GymAPI(ReversibleViewSet, CreateUGCMixin, UpdateModelMixin,
             DestroyUGCMixin):
    """Rest API for adding and updating gyms, and listing gym names"""
    basename = 'gym'
    queryset = Gym.objects.filter(is_active=True)
    serializer_class = GymSerializer

    def create(self, request, *args, **kwargs):
        instance = Gym.objects\
            .filter(is_active=False, name=request.data['name']).first()
        if instance is not None:
            instance.is_active = True
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response(serializer.data, status=HTTP_201_CREATED,
                        headers=self.get_success_headers(serializer.data))

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Gets the names of all active gyms
        :param request: the gym names GET request
        :return: the gym names
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = GymNameSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if self.request.user != instance.created_by:
            raise PermissionDenied()
        super().perform_destroy(instance)
        for boulder in instance.boulder_set.active():
            super().perform_destroy(boulder)
            boulder.ascent_set.deactivate_all(self.request.user)
        instance.favoritegym_set.deactivate_all(self.request.user)
        instance.grade_set.deactivate_all(self.request.user)


class FavoriteGymAPI(ReversibleViewSet, CreateUGCMixin, DestroyUGCMixin,
                     ListModelMixin):
    """Rest API for adding favorite gyms"""
    basename = 'favorite-gym'
    serializer_class = FavoriteGymSerializer
    lookup_field = 'gym__name'

    def get_queryset(self):
        return FavoriteGym.objects.filter(created_by=self.request.user,
                                          is_active=True)

    def perform_create(self, serializer, **kwargs):
        super().perform_create(
            serializer, gym=Gym.objects.get(
                name=self.request.data['gym']))


class BoulderAPI(ReversibleViewSet, CreateUGCMixin, DestroyUGCMixin,
                 UpdateModelMixin):
    """Rest API for reading and creating boulders in a specific gym"""
    basename = 'boulder'
    queryset = Boulder.objects.all()
    serializer_class = BoulderSerializer

    def perform_create(self, serializer, **kwargs):
        super().perform_create(
            serializer, gym=Gym.objects.get(pk=self.kwargs['gym_pk']))

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class AscentAPI(ReversibleViewSet, CreateUGCMixin):
    """Rest API for reading and creating boulders in a specific gym"""
    basename = 'ascent'
    queryset = Ascent.objects.all()
    serializer_class = AscentSerializer

    def perform_create(self, serializer, **kwargs):
        boulder_id = self.kwargs['boulder_pk']
        previous_ascents = Ascent.objects.filter(
            boulder__pk=boulder_id, created_by=self.request.user,
            is_active=True)
        for ascent in previous_ascents:
            ascent.is_active = False
        Ascent.objects.bulk_update(previous_ascents, ['is_active'])
        super().perform_create(
            serializer,
            boulder=Boulder.objects.get(pk=boulder_id))


class GymMapResourcesAPI(ReversibleViewSet):
    """
    API for serving all data required for populating a map of a gym:
    - The gym
    - The gym's active boulders
    - The user's ascent results for the active boulders
    """
    basename = 'gym-map-resources'
    serializer_class = GymMapResourcesSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']

    def list(self, request, *args, **kwargs):
        """
        Provides the gym map resources for the gym specified in the url
        :param request: the gym map resources GET request
        :return: the gym map resources
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def get_queryset(self):
        gym = self.filter_queryset(Gym.objects.all()).first()
        boulders = Boulder.objects.filter(gym=gym, is_active=True)
        boulder_features = [
            {'boulder': boulder,
             'ascent': boulder.ascent_set.filter(
                 created_by=self.request.user.pk,
                 is_active=True,
             ).first()}
            for boulder in boulders]
        return {
            'gym': gym,
            'boulder_features': boulder_features,
        }


def index(request):
    """
    View for vue frontend index page
    :param request: Incoming http request
    :return: rendered vue index page
    """
    return render(request, template_name='index.html')
