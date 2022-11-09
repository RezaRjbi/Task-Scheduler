from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from task_scheduler.settings import PHONE_REGEX


class User(AbstractUser):
    """
    extends the default django user model and add a phone field to it
    """
    Phone = models.CharField(max_length=13, validators=[RegexValidator(regex=PHONE_REGEX)])
