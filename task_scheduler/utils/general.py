import string
import random

from rest_framework import status
from rest_framework.response import Response


def generate_random_number(length):
    return int("".join([random.choice(list(string.digits)) for _ in range(length)]))


def response(status_code, instance=None, detail=None, errors=None, serializer=None, many=False, **kwargs):
    """
    generate Response objects for API response
    """
    response_body = dict()
    if instance:
        if not serializer:
            raise Exception("serializer for instance not provided")
        serialized_instance = serializer(instance, many=many)
        response_body["instances"] = serialized_instance.data
    if detail:
        response_body["detail"] = detail
    if errors:
        response_body["errors"] = errors
    response_body.update(**kwargs)
    return Response(data=response_body, status=status_code)


def unauthorized():
    return Response(data={"detail": "User inactive or deleted"}, status=status.HTTP_401_UNAUTHORIZED)
