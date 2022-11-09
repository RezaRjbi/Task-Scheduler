import string
import random


def generate_random_number(length):
    return int("".join([random.choice(list(string.digits)) for _ in range(length)]))
