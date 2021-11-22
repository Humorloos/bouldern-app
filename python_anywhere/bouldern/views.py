"""Module containing the views of the bouldern app"""
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from python_anywhere.bouldern.forms import GymMapFormSet, BoulderForm, ColorForm, GymForm, \
    DifficultyLevelFormset
from python_anywhere.bouldern.models import Boulder, Gym


def index(request):
    """Index page view"""
    if request.method == 'GET':
        return HttpResponse("Hello, world. You're at the bouldern index.")
    return HttpResponseNotFound()


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
            form.save()
        return HttpResponseRedirect(reverse(AddGym.name))


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
            gym_form.save()
            for difficulty_level_form in difficulty_level_formset:
                difficulty_level_form.save()
            # redirect to a new URL: (in my case the same, but empty again)
            return HttpResponseRedirect(reverse(index))
        return HttpResponseRedirect(reverse(self.name))


def gym_map(request, gym: str):
    """Gym map view"""
    gym_object = Gym.objects.filter(name=gym).get()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset: GymMapFormSet = GymMapFormSet(
            form_kwargs={'gym': gym_object},
            data=request.POST)
        # check whether it's valid:
        if formset.is_valid():
            form: BoulderForm
            for form in formset.forms:
                form.save()
            # redirect to a new URL: (in my case the same, but empty again)
            return HttpResponseRedirect(
                reverse(gym_map, kwargs={'gym': gym}))

    # if a GET (or any other method) we'll create a blank form
    else:
        formset = GymMapFormSet(form_kwargs={'gym': gym_object},
                                queryset=Boulder.objects.filter(
                                    gym__name__exact=gym))

    context = {
        'formset': formset,
        'gym': gym,
        'module': f'geodjango_{gym}',
        'gym_map': gym_object.map
    }
    return render(request, 'bouldern/gym_map_form.html', context)
