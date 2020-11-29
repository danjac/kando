# Standard Library
import mimetypes

# Django
from django.conf import settings
from django.db import models

# Third Party Libraries
from model_utils.models import TimeStampedModel

# Kando
from kando.cards.models import Card
from kando.projects.models import Project


def file_upload_path(instance, filename):
    return f"project/{instance.card.project.id}/attachments/{filename}"


class Attachment(TimeStampedModel):
    # attachment may be directly to a project, or project+card.
    # e.g. project might have "global" docs such as NDA, specs
    # but card might also have its own attachments
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, null=True, blank=True, on_delete=models.SET_NULL
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    file = models.FileField(upload_to=file_upload_path)
    media_type = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        _, media_type = mimetypes.guess_type(self.file.name)
        self.media_type = media_type
        return super().save(*args, **kwargs)
