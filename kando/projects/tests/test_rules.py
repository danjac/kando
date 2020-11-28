# Third Party Libraries
import pytest

# Local
from ..factories import ProjectFactory, ProjectMemberFactory
from ..models import ProjectMember
from ..rules import (
    is_project_admin,
    is_project_manager,
    is_project_member,
    is_project_owner,
)

pytestmark = pytest.mark.django_db


class TestIsProjectOwner:
    def test_is_owner(self, project):
        assert is_project_owner(project.owner, project)

    def test_is_not_owner(self, user):
        project = ProjectFactory()
        assert not is_project_owner(user, project)

    def test_anonymous_is_not_owner(self, anonymous_user, project):
        assert not is_project_owner(anonymous_user, project)


class TestIsProjectMember:
    def test_is_member(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MEMBER)
        assert is_project_member(user, member.project)

    def test_is_not_member(self, user):
        assert not is_project_member(user, ProjectFactory())

    def test_anonymous_is_not_member(self, anonymous_user, project):
        assert not is_project_member(anonymous_user, project)


class TestIsProjectManager:
    def test_is_manager(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MANAGER)
        assert is_project_manager(user, member.project)

    def test_is_not_manager(self, user):
        assert not is_project_manager(user, ProjectFactory())

    def test_anonymous_is_not_manager(self, anonymous_user, project):
        assert not is_project_manager(anonymous_user, project)


class TestIsProjectAdmin:
    def test_is_admin(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.ADMIN)
        assert is_project_admin(user, member.project)

    def test_is_not_admin(self, user):
        assert not is_project_admin(user, ProjectFactory())

    def test_anonymous_is_not_admin(self, anonymous_user, project):
        assert not is_project_admin(anonymous_user, project)


class TestPermissions:
    def test_project_owner(self, project):
        assert project.owner.has_perm("projects.view_project", project)
        assert project.owner.has_perm("projects.change_project", project)
        assert project.owner.has_perm("projects.delete_project", project)

    def test_anonymous_user(self, anonymous_user, project):
        assert not anonymous_user.has_perm("projects.view_project", project)
        assert not anonymous_user.has_perm("projects.change_project", project)
        assert not anonymous_user.has_perm("projects.delete_project", project)
