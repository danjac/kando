# Django
from django.db import models

# Third Party Libraries
from model_utils.models import TimeStampedModel

# Kando
from kando.projects.models import Project


class Column(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # swimlane (NULL)
    name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    show_in_dashboard = models.BooleanField(default=True)

    def __str__(self):
        return self.name
