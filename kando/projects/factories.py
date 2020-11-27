# Third Party Libraries
import factory
from factory.django import DjangoModelFactory

# Kando
from kando.users.factories import UserFactory

# Local
from .models import Project, ProjectMember


class ProjectFactory(DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Project


class ProjectMemberFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = ProjectMember
