"""Module containing the views of the bouldern app"""
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.views import View
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from url_filter.integrations.drf import DjangoFilterBackend

from python_anywhere.bouldern.forms import GymMapFormSet, BoulderForm, \
    ColorForm, GymForm, DifficultyLevelFormset
from python_anywhere.bouldern.models import Boulder, Gym, Color
from python_anywhere.bouldern.serializers import GymSerializer, ColorSerializer, \
    BoulderSerializer


class ReversibleViewSet(GenericViewSet):
    """
    VewSet base class that allows using ViewSet().reverse_action() for
    retrieving view URLs.
    """
    basename = None
    request = None

    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        basename = cls.basename
        view = super().as_view(actions, **initkwargs)
        cls.basename = basename
        return view


class AddColor(View):
    """View for adding new colors"""
    name = 'add_color'
    form_class = ColorForm

    def post(self, request):
        """
        Verifies incoming color forms and persists them if valid
        :param request: incoming request with color form
        :return: redirect response to bouldern index
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save_for_user(request.user)
        return HttpResponseRedirect(reverse(AddGym.name))


class ColorAPI(ReversibleViewSet, ListModelMixin, CreateModelMixin):
    """REST API for adding colors"""
    basename = 'color'
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AddGym(View):
    """View for adding new gyms with their specific difficulty levels"""
    name = 'add_gym'
    template_name = 'bouldern/gym_form.html'
    form_class = GymForm

    def get(self, request):
        """
        Gets the rendered gym form
        :param request: incoming get request
        :return: response with the rendered gym form
        """
        difficulty_level_formset = DifficultyLevelFormset()
        gym_form = self.form_class()
        color_form = ColorForm()
        context = {
            'color_form': color_form,
            'difficulty_level_formset': difficulty_level_formset,
            'gym_form': gym_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Verifies incoming gym form and difficulty level formset and persists
        the data if it is valid.
        :param request: incoming post request with form data
        :return: redirect to index if form was valid, else redirect to gym form
        """
        gym_form = self.form_class(data=request.POST, files=request.FILES)
        difficulty_level_formset = DifficultyLevelFormset(
            data=request.POST, instance=gym_form.instance)
        # check whether it's valid:
        if gym_form.is_valid() and difficulty_level_formset.is_valid():
            gym_form.save_for_user(request.user)
            for difficulty_level_form in difficulty_level_formset:
                difficulty_level_form.save_for_user(request.user)
            # redirect to a new URL: (in my case the same, but empty again)
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse(self.name))


class GymAPI(ReversibleViewSet, ModelViewSet):
    """Rest API for adding gyms"""
    basename = 'gym'
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BoulderAPI(ReversibleViewSet, ListModelMixin, CreateModelMixin):
    """Rest API for reading and creating boulders in a specific gym"""
    basename = 'boulder'
    queryset = Boulder.objects.all()
    serializer_class = BoulderSerializer

    def get_queryset(self):
        return Boulder.objects.filter(gym_id=self.kwargs['gym_pk'])

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user,
                        gym=Gym.objects.get(pk=self.kwargs['gym_pk']))


def gym_map(request: WSGIRequest, gym_name: str):
    """Gym map view"""
    gym = Gym.objects.filter(name=gym_name).get()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset: GymMapFormSet = GymMapFormSet(
            form_kwargs={'gym': gym},
            data=request.POST)
        # check whether it's valid:
        if formset.is_valid():
            form: BoulderForm
            for form in formset.forms:
                form.save_for_user(request.user)
            # redirect to a new URL: (in my case the same, but empty again)
            return HttpResponseRedirect(
                reverse(gym_map, kwargs={'gym_name': gym_name}))

    # if a GET (or any other method) we'll create a blank form
    else:
        formset = GymMapFormSet(
            form_kwargs={'gym': gym},
            queryset=Boulder.objects.filter(gym__name__exact=gym_name))

    context = {
        'formset': formset,
        'gym': gym_name,
        'module': f'geodjango_{gym_name}',
        'gym_map': gym.map
    }
    return render(request, 'bouldern/gym_map_form.html', context)


def index(request):
    """
    View for vue frontend index page
    :param request: Incoming http request
    :return: rendered vue index page
    """
    return render(request, template_name='index.html')
