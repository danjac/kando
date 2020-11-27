# Third Party Libraries
import pytest

# Kando
from kando.users.factories import UserFactory

# Local
from ..factories import ProjectMemberFactory
from ..models import Project

pytestmark = pytest.mark.django_db


class TestProjectManager:
    def test_create_project(self, user):
        project = Project.objects.create_project("test project", user, is_private=True)
        assert project.owner == user
        assert project.is_private
        assert project.column_set.count() == 4

        columns = project.column_set.order_by("position")
        assert columns[0].name == "Backlog"
        assert columns[0].position == 1

    def test_accessible_to_if_owner(self, project):
        assert Project.objects.accessible_to(project.owner).count() == 1

    def test_accessible_to_if_not_owner(self, project):
        assert Project.objects.accessible_to(UserFactory()).count() == 0

    def test_accessible_to_if_member(self, user):
        ProjectMemberFactory(user=user)
        assert Project.objects.accessible_to(user).count() == 1

    def test_accessible_to_if_inactive_member(self, user):
        ProjectMemberFactory(user=user, is_active=False)
        assert Project.objects.accessible_to(user).count() == 0
