# Third Party Libraries
import factory
from factory.django import DjangoModelFactory

# Kando
from kando.users.factories import UserFactory

# Local
from .models import Project


class ProjectFactory(DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Project
