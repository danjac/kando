# Third Party Libraries
import pytest

# Local
from ..forms import ProjectCreationForm

pytestmark = pytest.mark.django_db


class TestProjectCreationForm:
    def test_create_project(self, user):

        data = {
            "name": "test project",
            "description": "test",
            "is_private": False,
            "task_limit": 10,
        }
        form = ProjectCreationForm(data)
        assert form.is_valid()
        project = form.save(user)
        assert project.owner == user
        assert project.name == "test project"
        assert project.column_set.count() == 4
