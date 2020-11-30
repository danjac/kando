# Third Party Libraries
import pytest

# Kando
from kando.projects.factories import ProjectMemberFactory
from kando.projects.models import ProjectMember
from kando.users.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestPermissions:
    def test_anonymous_user(self, anonymous_user, column):

        assert not anonymous_user.has_perm("columns.create_column", column.project)
        assert not anonymous_user.has_perm("columns.move_columns", column.project)
        assert not anonymous_user.has_perm("columns.view_column", column)
        assert not anonymous_user.has_perm("columns.change_column", column)
        assert not anonymous_user.has_perm("columns.delete_column", column)

    def test_non_project_member(self, column):
        user = UserFactory()
        assert not user.has_perm("columns.create_column", column.project)
        assert not user.has_perm("columns.move_columns", column.project)
        assert not user.has_perm("columns.view_column", column)
        assert not user.has_perm("columns.change_column", column)
        assert not user.has_perm("columns.delete_column", column)

    def test_project_member(self, column):
        user = UserFactory()
        ProjectMemberFactory(user=user, project=column.project)
        assert not user.has_perm("columns.create_column", column.project)
        assert not user.has_perm("columns.move_columns", column.project)
        assert user.has_perm("columns.view_column", column)
        assert not user.has_perm("columns.change_column", column)
        assert not user.has_perm("columns.delete_column", column)

    def test_project_manager(self, column):
        user = UserFactory()
        ProjectMemberFactory(
            user=user, project=column.project, role=ProjectMember.Role.MANAGER
        )
        assert not user.has_perm("columns.create_column", column.project)
        assert not user.has_perm("columns.move_columns", column.project)
        assert user.has_perm("columns.view_column", column)
        assert not user.has_perm("columns.change_column", column)
        assert not user.has_perm("columns.delete_column", column)

    def test_project_admin(self, column):
        user = UserFactory()
        ProjectMemberFactory(
            user=user, project=column.project, role=ProjectMember.Role.ADMIN
        )
        assert user.has_perm("columns.create_column", column.project)
        assert user.has_perm("columns.move_columns", column.project)
        assert user.has_perm("columns.view_column", column)
        assert user.has_perm("columns.change_column", column)
        assert user.has_perm("columns.delete_column", column)

    def test_project_owner(self, column):
        assert column.project.owner.has_perm("columns.create_column", column.project)
        assert column.project.owner.has_perm("columns.move_columns", column.project)
        assert column.project.owner.has_perm("columns.view_column", column)
        assert column.project.owner.has_perm("columns.change_column", column)
        assert column.project.owner.has_perm("columns.delete_column", column)
