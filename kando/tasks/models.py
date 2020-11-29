# Django
from django.conf import settings
from django.db import models

# Third Party Libraries
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel

# Kando
from kando.cards.models import Card


class Task(TimeStampedModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    description = models.CharField(max_length=500)
    position = models.IntegerField(default=0)
    completed = models.DateTimeField(null=True, blank=True)

    tracker = FieldTracker(fields=["card"])

    def save(self, *args, **kwargs):
        if not self.position or self.tracker.has_changed("card"):
            self.position = (
                self.card.task_set.aggregate(models.Max("position"))["position__max"]
                or 0
            ) + 1
        return super().save(*args, **kwargs)
