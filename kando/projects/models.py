# Django
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

# Third Party Libraries
from model_utils.models import TimeStampedModel


class ProjectQuerySet(models.QuerySet):
    def accessible_to(self, user):
        """Returns all projects a user is a member of,
        either owner or member group/user"""
        # for now we just have owners
        return self.filter(owner=user)


class ProjectManager(models.Manager.from_queryset(ProjectQuerySet)):
    def create_project(self, name, owner, **kwargs):
        """Creates a new project with default columns """

        project = self.create(name=name, owner=owner, **kwargs)

        for position, name in enumerate(
            (_("Backlog"), _("Ready"), ("In Progress"), _("Done")), 1
        ):
            project.column_set.create(name=name, position=position)

        return project


class Project(TimeStampedModel):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    task_limit = models.IntegerField(default=0)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    objects = ProjectManager()

    def __str__(self):
        return self.name
