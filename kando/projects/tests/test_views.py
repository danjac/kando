# Django
from django.urls import reverse

# Third Party Libraries
import pytest

# Local
from ..factories import ProjectFactory
from ..models import Project

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
            "is_private": False,
            "task_limit": 10,
        }

        response = client.post(reverse("projects:create_project"), data)
        project = Project.objects.get()

        assert response.url == project.get_absolute_url()
        assert project.owner == login_user
