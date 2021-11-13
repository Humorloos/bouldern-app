"""This module contains the views of the calendar app"""
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from googleCalendarApp.calendar_handler import CalendarHandler
from python_anywhere.calendar_app.constants import CHANNEL_ID_KEY


@csrf_exempt
def handle_calendar_update(request):
    """
    Handles messages from google calendar calling CalendarHandler with the
    incoming data
    :param request: The incoming request
    :return:
    """
    # only react to calendar API channel posts
    if CHANNEL_ID_KEY not in request.headers.keys():
        return HttpResponse("Hello, world. You're at the bouldern index.")
    CalendarHandler().post(request.headers.get(CHANNEL_ID_KEY))
    return HttpResponse(status=200)
