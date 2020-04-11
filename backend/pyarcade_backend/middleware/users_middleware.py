from django.http import JsonResponse

import json


class UserLoginMiddleware:
    ALLOWED_PATHS = {
        "/users/signup/",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != "POST" or \
           request.path not in UserLoginMiddleware.ALLOWED_PATHS:
            return self.get_response(request)

        try:
            body = json.loads(request.body)

            # POST missing needed body keys
            if "username" not in body or "password" not in body:
                raise Exception("missing body parameters")

        except (ValueError, Exception):
            return JsonResponse({
                "message": "Did not meet requirements."
            }, status=400)

        username = body["username"]
        password = body["password"]

        request.validated = {
            "username": username,
            "password": password,
        }

        return self.get_response(request)
