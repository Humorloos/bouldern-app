"""Module containing the views of the bouldern app"""
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework.generics import ListCreateAPIView, CreateAPIView

from python_anywhere.bouldern.forms import GymMapFormSet, BoulderForm, \
    ColorForm, GymForm, DifficultyLevelFormset
from python_anywhere.bouldern.models import Boulder, Gym, Color
from python_anywhere.bouldern.serializers import GymSerializer, ColorSerializer


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


class AddColorRest(CreateAPIView):
    """REST API for adding colors"""
    name = 'add_color_rest'
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class AddGymRest(ListCreateAPIView):
    """Rest API for adding gyms"""
    name = 'add_gym_rest'
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
