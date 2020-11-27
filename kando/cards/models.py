# Django
from django.conf import settings
from django.db import models

# Third Party Libraries
from model_utils.models import TimeStampedModel

# Kando
from kando.columns.models import Column
from kando.projects.models import Project


class Card(TimeStampedModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="owned_cards",
    )

    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="assigned_cards",
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=0)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)

    complexity = models.PositiveIntegerField(default=1)
    priority = models.PositiveIntegerField(default=1)

    hours_estimated = models.PositiveIntegerField(default=0)
    hours_spent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
