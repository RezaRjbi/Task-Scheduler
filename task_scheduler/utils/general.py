import string
import random

from rest_framework.response import Response
from django.forms.models import model_to_dict


def generate_random_number(length):
    return int("".join([random.choice(list(string.digits)) for _ in range(length)]))


def response(instance=None, data=None, errors=None, status_code=None, serializer=None, many=False, **kwargs):
    if instance and not serializer:
        raise Exception("serializer for instance not provided")
    response_body = {
        "data": data,
        "errors": errors,
    }
    if instance:
        serialized_instance = serializer(instance, many=many)
        response_body["instances"] = serialized_instance.data
    if kwargs:
        response_body.update(**kwargs)
    return Response(data=response_body, status=status_code)
