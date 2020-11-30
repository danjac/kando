# Django
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render

# Local
from ..http import Http400


class HttpResponseBadRequestExceptionMiddleware:
    """Handles Http400 exceptions"""

    template_name = "400.html"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            return self.get_response(request)
        except Http400 as e:
            return HttpResponseBadRequest(str(e))


class HttpResponseNotAllowedMiddleware:
    """
    Renders a custom 405 template if settings.DEBUG = False.
    """

    template_name = "405.html"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseNotAllowed) and not settings.DEBUG:
            return render(request, self.template_name, status=405)
        return response
