"""Module containing the views of the bouldern app"""
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from url_filter.integrations.drf import DjangoFilterBackend

from python_anywhere.bouldern.models import Boulder, Gym, Color
from python_anywhere.bouldern.serializers import GymSerializer, ColorSerializer, \
    BoulderSerializer
from python_anywhere.views import ReversibleViewSet


class CreateUGCMixin(CreateModelMixin, GenericViewSet):
    """Mixin for creating UGC instances"""

    def perform_create(self, serializer, **kwargs):
        serializer.save(created_by=self.request.user,
                        modified_by=self.request.user,
                        **kwargs)


class ColorAPI(ReversibleViewSet, ListModelMixin, CreateUGCMixin):
    """REST API for adding colors"""
    basename = 'color'
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class GymAPI(ReversibleViewSet, ModelViewSet, CreateUGCMixin):
    """Rest API for adding gyms"""
    basename = 'gym'
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']


class BoulderAPI(ReversibleViewSet, ModelViewSet, CreateUGCMixin):
    """Rest API for reading and creating boulders in a specific gym"""
    basename = 'boulder'
    queryset = Boulder.objects.all()
    serializer_class = BoulderSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['is_active']

    def get_queryset(self):
        return Boulder.objects.filter(gym_id=self.kwargs['gym_pk'])

    def perform_create(self, serializer, **kwargs):
        super().perform_create(
            serializer, gym=Gym.objects.get(pk=self.kwargs['gym_pk']))


def index(request):
    """
    View for vue frontend index page
    :param request: Incoming http request
    :return: rendered vue index page
    """
    return render(request, template_name='index.html')
