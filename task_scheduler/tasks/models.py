from django.db import models
from utils.general import generate_random_number
from django.core.validators import MaxValueValidator, ValidationError

from users.models import User


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.IntegerField(validators=[MaxValueValidator(99999999)], unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.deadline:
            if self.deadline < self.created_date:
                raise ValidationError("deadline must be greater than created date")
        generated_task_id = generate_random_number(8)

        while Task.objects.filter(task_id=generated_task_id).exists():
            generated_task_id = generate_random_number(8)

        self.task_id = generated_task_id
        super(Task, self).save(*args, **kwargs)