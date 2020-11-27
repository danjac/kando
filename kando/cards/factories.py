# Third Party Libraries
import factory
from factory.django import DjangoModelFactory

# Kando
from kando.columns.factories import ColumnFactory
from kando.projects.factories import ProjectFactory
from kando.users.factories import UserFactory

# Local
from .models import Card


class ColumnFactory(DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    column = factory.SubFactory(ColumnFactory)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Card
