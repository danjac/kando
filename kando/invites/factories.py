# Third Party Libraries
import factory
from factory.django import DjangoModelFactory

# Kando
from kando.projects.factories import ProjectFactory
from kando.users.factories import UserFactory

# Local
from .models import Invite


class InviteFactory(DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    sender = factory.SubFactory(UserFactory)

    class Meta:
        model = Invite
