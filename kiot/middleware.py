from django.shortcuts import redirect
from django.http import JsonResponse


class HTMX401RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 401 and request.headers.get("HX-Request"):
            response["HX-Redirect"] = "/login/"

        return response
