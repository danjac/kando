# Django
from django.core.exceptions import PermissionDenied

# Third Party Libraries
import pytest

# Local
from ..factories import UserFactory
from ..utils import has_perm_or_403

pytestmark = pytest.mark.django_db


class TestHasPermOr403:
    def test_has_permission(self, project):
        has_perm_or_403(project.owner, "projects.change_project", project)

    def test_no_permission(self, project):
        user = UserFactory()
        with pytest.raises(PermissionDenied):
            has_perm_or_403(user, "projects.change_project", project)

    def test_anonymous_user(self, anonymous_user, project):
        with pytest.raises(PermissionDenied):
            has_perm_or_403(anonymous_user, "projects.change_project", project)
