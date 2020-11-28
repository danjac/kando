# Third Party Libraries
import pytest

# Local
from ..rules import is_project_owner

pytestmark = pytest.mark.django_db


class TestIsProjectOwner:
    def test_is_owner(self, project):
        assert is_project_owner(project.owner, project)
