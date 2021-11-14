"""Module containing the views of the bouldern app"""
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .forms import GymMapFormSet, BoulderForm
from .models import Boulder, Gym


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
        formset = GymMapFormSet(
            queryset=Boulder.objects.filter(gym__name__exact=gym))

    context = {
        'formset': formset,
        'gym': gym,
        'module': f'geodjango_{gym}',
        'gym_map': Gym.objects.filter(name=gym).only('map').get().map
    }
    return render(request, 'bouldern/gym_map_form.html', context)
