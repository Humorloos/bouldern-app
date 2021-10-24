from django.http import HttpResponse

from bouldernFormsApp.gym_handler import GymHandler


def index(request):
    return HttpResponse("Hello, world. You're at the bouldern index.")


def handle_gym_update(request, gym):
    GymHandler(gym).post()
