# Third Party Libraries
import pytest

# Local
from ..factories import ProjectFactory, ProjectMemberFactory
from ..models import ProjectMember

pytestmark = pytest.mark.django_db


class TestProjectMemberPermissions:
    def test_project_owner(self, member):
        assert member.project.owner.has_perm("projects.add_members", member.project)
        assert member.project.owner.has_perm("projects.change_member_role", member)
        assert member.project.owner.has_perm("projects.remove_member", member)

    def test_anonymous_user(self, anonymous_user, member):
        assert not anonymous_user.has_perm("projects.add_members", member.project)
        assert not anonymous_user.has_perm("projects.change_member_role", member)
        assert not anonymous_user.has_perm("projects.remove_member", member)

    def test_non_member(self, user):
        member = ProjectMemberFactory()
        assert not user.has_perm("projects.add_members", member.project)
        assert not user.has_perm("projects.change_member_role", member)
        assert not user.has_perm("projects.remove_member", member)

    def test_member(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MEMBER)
        assert not user.has_perm("projects.add_members", member.project)
        assert not user.has_perm("projects.change_member_role", member)
        assert not user.has_perm("projects.remove_member", member)

    def test_manager(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MANAGER)
        assert not user.has_perm("projects.add_members", member.project)
        assert not user.has_perm("projects.change_member_role", member)
        assert not user.has_perm("projects.remove_member", member)

    def test_admin(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.ADMIN)
        assert user.has_perm("projects.add_members", member.project)
        assert member.project.owner.has_perm("projects.change_member_role", member)
        assert member.project.owner.has_perm("projects.remove_member", member)


class TestProjectPermissions:
    def test_project_owner(self, project):
        assert project.owner.has_perm("projects.view_project", project)
        assert project.owner.has_perm("projects.change_project", project)
        assert project.owner.has_perm("projects.delete_project", project)

    def test_anonymous_user(self, anonymous_user, project):
        assert not anonymous_user.has_perm("projects.view_project", project)
        assert not anonymous_user.has_perm("projects.change_project", project)
        assert not anonymous_user.has_perm("projects.delete_project", project)

    def test_non_member(self, user):
        project = ProjectFactory()
        assert not user.has_perm("projects.view_project", project)
        assert not user.has_perm("projects.change_project", project)
        assert not user.has_perm("projects.delete_project", project)

    def test_member(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MEMBER)
        assert user.has_perm("projects.view_project", member.project)
        assert not user.has_perm("projects.change_project", member.project)
        assert not user.has_perm("projects.delete_project", member.project)

    def test_manager(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MANAGER)
        assert user.has_perm("projects.view_project", member.project)
        assert not user.has_perm("projects.change_project", member.project)
        assert not user.has_perm("projects.delete_project", member.project)

    def test_admin(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.ADMIN)
        assert user.has_perm("projects.view_project", member.project)
        assert user.has_perm("projects.change_project", member.project)
        assert not user.has_perm("projects.delete_project", member.project)
