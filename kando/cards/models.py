# Django
from django.conf import settings
from django.db import models
from django.urls import reverse

# Third Party Libraries
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel

# Kando
from kando.columns.models import Column
from kando.projects.models import Project


class CardQuerySet(models.QuerySet):
    def accessible_to(self, user):
        """Returns all projects a user is a member of,
        either owner or member"""
        return self.filter(
            models.Q(project__owner=user)
            | models.Q(
                project__projectmember__user=user,
                project__projectmember__is_active=True,
            )
        )


class CardManager(models.Manager.from_queryset(CardQuerySet)):
    ...


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

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_cards",
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

    objects = CardManager()

    tracker = FieldTracker(fields=["column"])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cards:card_detail", args=[self.id])

    def save(self, *args, **kwargs):
        if not self.position or self.tracker.has_changed("column"):
            self.position = (
                self.column.card_set.aggregate(models.Max("position"))["position__max"]
                or 0
            ) + 1
        return super().save(*args, **kwargs)
