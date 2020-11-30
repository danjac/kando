# Django
from django.db import models

# Third Party Libraries
from model_utils.models import TimeStampedModel

# Kando
from kando.projects.models import Project


class Column(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    position = models.IntegerField(default=0)
    show_in_dashboard = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.position:
            self.position = (
                self.project.column_set.aggregate(models.Max("position"))[
                    "position__max"
                ]
                or 0
            ) + 1
        return super().save(*args, **kwargs)
