from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import GymMapForm


def index(request):
    return HttpResponse("Hello, world. You're at the bouldern index.")


def gym_map(request, gym: str):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GymMapForm(gym=gym, data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL: (in my case the same, but empty again)
            return HttpResponseRedirect(
                reverse('bouldern:map', kwargs={'gym': gym}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GymMapForm(gym=gym)

    context = {
        'form': form,
        'gym': gym,
    }
    return render(request, 'bouldern/gym_map_form.html', context)
