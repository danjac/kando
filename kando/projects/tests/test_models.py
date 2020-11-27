# Third Party Libraries
import pytest

# Local
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
