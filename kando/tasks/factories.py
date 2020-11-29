# Third Party Libraries
import factory
from factory.django import DjangoModelFactory

# Kando
from kando.cards.factories import CardFactory
from kando.users.factories import UserFactory

# Local
from .models import Task


class TaskFactory(DjangoModelFactory):
    card = factory.SubFactory(CardFactory)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Task
