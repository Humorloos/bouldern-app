"""Module containing the views of the bouldern app"""
from PIL import Image
from django.contrib.staticfiles.finders import find
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .forms import GymMapFormSet, BoulderForm


def index(request):
    """Index page view"""
    if request.method == 'GET':
        return HttpResponse("Hello, world. You're at the bouldern index.")
    return HttpResponseNotFound()


def gym_map(request, gym: str):
    """Gym map view"""
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset: GymMapFormSet = GymMapFormSet(data=request.POST)
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
        formset = GymMapFormSet()

    map_width, map_height = Image.open(
        find(f'bouldern/images/{gym}/hallenplan.png')).size

    context = {
        'formset': formset,
        'gym': gym,
        'module': f'geodjango_{gym}',
        'map_width': map_width,
        'map_height': map_height
    }
    return render(request, 'bouldern/gym_map_form.html', context)
