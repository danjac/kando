# Django
from django.conf import settings
from django.db import models

# Third Party Libraries
from model_utils.models import TimeStampedModel


class Project(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    task_limit = models.IntegerField(default=0)

    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
