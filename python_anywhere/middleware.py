"""
source: https://github.com/iMerica/dj-rest-auth/issues/97#issuecomment-739942573
"""
import json
import logging

from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from python_anywhere.settings import JWT_AUTH_REFRESH_COOKIE


class MoveJWTRefreshCookieIntoTheBody(MiddlewareMixin):
    """
    For Django Rest Framework JWT's POST "/token-refresh" endpoint. Check
    for a 'refresh' in the request.COOKIES and if there, move it to the body payload.
    """

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    # noinspection PyMethodMayBeStatic
    # pylint: disable=unused-argument,no-self-use
    def process_view(self, request: HttpRequest, view_func, *view_args,
                     **view_kwargs):
        """
        This function is called just before Django calls the view
        :param request:
        :param view_func: python function that django is about to use
        :param view_args: list of positional arguments that will be passed to the view
        :param view_kwargs: dictionary of keyword arguments that will be passed to the view
        """
        if request.path == '/token/refresh/' and \
                JWT_AUTH_REFRESH_COOKIE in request.COOKIES:
            if request.body != b'':
                data = json.loads(request.body)
                data['refresh'] = request.COOKIES[JWT_AUTH_REFRESH_COOKIE]
                # pylint: disable=protected-access
                request._body = json.dumps(data).encode('utf-8')
            else:
                logging.info(
                    "The incoming request body must be set to an empty object.")
