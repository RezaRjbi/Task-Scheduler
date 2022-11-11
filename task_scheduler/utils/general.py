import string
import random

from rest_framework.response import Response
from django.forms.models import model_to_dict


def generate_random_number(length):
    return int("".join([random.choice(list(string.digits)) for _ in range(length)]))


def response(instance=None, data=None, errors=None, status_code=None, to_dict=False, **kwargs):
    response_body = {
        "data": data,
        "errors": errors,
    }
    if instance:
        if to_dict:
            instance = model_to_dict(instance)
        response_body["instance(s)"] = instance
    if kwargs:
        response_body.update(**kwargs)
    return Response(data=response_body, status=status_code)
