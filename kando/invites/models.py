# Standard Library
import uuid

# Django
from django.conf import settings
from django.db import models
from django.utils import timezone

# Third Party Libraries
from model_utils.models import TimeStampedModel

# Kando
from kando.projects.models import Project, ProjectMember


class Invite(TimeStampedModel):
    class AlreadyMember(ValueError):
        ...

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_invites"
    )

    invitee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="accepted_invites",
    )

    accepted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.guid

    def accept(self, user):
        if ProjectMember.objects.filter(user=user, project=self.project).exists():
            raise self.AlreadyMember

        ProjectMember.objects.create(user=user, project=self.project)

        self.accepted = timezone.now()
        self.invitee = user
        self.save()
