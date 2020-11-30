# Django
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

# Third Party Libraries
from model_utils.models import TimeStampedModel


class ProjectQuerySet(models.QuerySet):
    def accessible_to(self, user):
        """Returns all projects a user is a member of,
        either owner or member"""
        return self.filter(
            models.Q(owner=user)
            | models.Q(projectmember__user=user, projectmember__is_active=True)
        )


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
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="owned_projects",
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProjectMember",
        blank=True,
        related_name="projects",
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    objects = ProjectManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:project_board", args=[self.id])


class ProjectMember(TimeStampedModel):
    class Role(models.TextChoices):
        # add tasks, edit/move own tasks, assign myself to tasks
        MEMBER = "member", _("Member")
        # edit others' tasks, assign tasks
        MANAGER = "manager", _("Manager")
        # add users to project, change columns, change permissions, edit project, delete project
        # owner has all these permissions by default
        ADMIN = "admin", _("Admin")

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(
        choices=Role.choices, max_length=12, default=Role.MEMBER, db_index=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_project_member", fields=["project", "user"]
            )
        ]

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse(
            "projects:member_detail", args=[self.project.id, self.user.username]
        )
