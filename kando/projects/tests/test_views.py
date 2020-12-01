# Django
from django.urls import reverse

# Third Party Libraries
import pytest

# Kando
from kando.cards.factories import CardFactory
from kando.columns.factories import ColumnFactory

# Local
from ..factories import ProjectFactory, ProjectMemberFactory
from ..models import Project, ProjectMember

pytestmark = pytest.mark.django_db


class TestProjectsOverview:
    def test_get(self, client, login_user):
        ProjectFactory.create_batch(3, owner=login_user)
        ProjectFactory()
        response = client.get(reverse("projects:projects_overview"))
        assert response.status_code == 200
        assert len(response.context["projects"]) == 3


class TestCreateProject:
    def test_get(self, client, login_user):
        response = client.get(reverse("projects:create_project"))
        assert response.status_code == 200

    def test_post(self, client, login_user):

        data = {
            "name": "test project",
            "description": "test",
        }

        response = client.post(reverse("projects:create_project"), data)
        project = Project.objects.get()

        assert response.url == project.get_absolute_url()
        assert project.owner == login_user


class TestProjectBoard:
    def test_get(self, client, login_user):
        project = ProjectFactory(owner=login_user, name="Test Project")
        for column in ColumnFactory.create_batch(3, project=project):
            CardFactory.create_batch(12, column=column, project=project)
        response = client.get(reverse("projects:project_board", args=[project.id]))
        assert response.status_code == 200


class TestDuplicateProject:
    def test_post(self, client, login_user):
        project = ProjectFactory(owner=login_user, name="Test Project")
        ColumnFactory.create_batch(3, project=project)

        response = client.post(reverse("projects:duplicate_project", args=[project.id]))
        dupe = Project.objects.exclude(pk=project.id).first()
        assert response.url == dupe.get_absolute_url()
        assert dupe.name == "[DUPLICATE] Test Project"
        assert dupe.owner == login_user
        assert dupe.column_set.count() == 3


class TestRemoveMember:
    def test_post(self, client, login_user):
        project = ProjectFactory(owner=login_user)
        member = ProjectMemberFactory(project=project)

        card = CardFactory(project=project, owner=member.user)

        response = client.post(reverse("projects:remove_member", args=[member.id]))
        assert response.url == reverse("projects:project_members", args=[project.id])
        assert ProjectMember.objects.count() == 0

        # ensure card ownership transferred to project owner
        card.refresh_from_db()
        assert card.owner == login_user
