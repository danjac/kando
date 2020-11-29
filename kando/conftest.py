# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse

# Third Party Libraries
import pytest

# Kando
from kando.cards.factories import CardFactory
from kando.columns.factories import ColumnFactory
from kando.invites.factories import InviteFactory
from kando.projects.factories import ProjectFactory, ProjectMemberFactory
from kando.tasks.factories import TaskFactory
from kando.users.factories import UserFactory


@pytest.fixture
def get_response():
    return lambda req: HttpResponse()


@pytest.fixture
def user_model():
    return get_user_model()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def login_user(client):
    password = "t3SzTP4sZ"
    user = UserFactory()
    user.set_password(password)
    user.save()
    client.login(username=user.username, password=password)
    return user


@pytest.fixture
def project(user):
    return ProjectFactory(owner=user)


@pytest.fixture
def member(project, login_user):
    return ProjectMemberFactory(project=project, user=login_user)


@pytest.fixture
def column(project):
    return ColumnFactory(project=project)


@pytest.fixture
def card(column):
    return CardFactory(
        project=column.project, column=column, owner=column.project.owner
    )


@pytest.fixture
def task(card):
    return TaskFactory(card=card, owner=card.owner)


@pytest.fixture
def invite(project):
    return InviteFactory(project=project)
