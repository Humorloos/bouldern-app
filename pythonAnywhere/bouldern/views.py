from PIL import Image
from django.contrib.staticfiles.finders import find
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import GymMapFormSet


def index(request):
    return HttpResponse("Hello, world. You're at the bouldern index.")


def gym_map(request, gym: str):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = GymMapFormSet(form_kwargs={'gym': gym}, data=request.POST)
        # check whether it's valid:
        if formset.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL: (in my case the same, but empty again)
            return HttpResponseRedirect(
                reverse('bouldern:map', kwargs={'gym': gym}))

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
