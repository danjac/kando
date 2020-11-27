# Third Party Libraries
import factory
from factory.django import DjangoModelFactory

# Kando
from kando.projects.factories import ProjectFactory

# Local
from .models import Column


class ColumnFactory(DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Column
