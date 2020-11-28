# Standard Library
import uuid

# Django
from django.conf import settings
from django.db import models
from django.utils import timezone

# Third Party Libraries
from model_utils.models import TimeStampedModel

# Kando
from kando.projects.models import Project


class Invite(TimeStampedModel):

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)

    accepted = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "unique_project_invite", fields=["project", "email"]
            )
        ]

    def __str__(self):
        return self.guid

    def accept(self, user):
        self.accepted = timezone.now()
        self.user = user
        self.save()
