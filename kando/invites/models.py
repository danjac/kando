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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_project_invite", fields=["project", "email"]
            )
        ]

    def __str__(self):
        return self.guid

    def accept(self, user):
        # check IntegrityError
        ProjectMember.objects.create(user=user, project=self.project)
        self.accepted = timezone.now()
        self.invitee = user
        self.save()
