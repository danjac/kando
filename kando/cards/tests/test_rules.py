# Third Party Libraries
import pytest

# Kando
from kando.projects.factories import ProjectMemberFactory
from kando.projects.models import ProjectMember
from kando.users.factories import UserFactory

# Local
from ..factories import CardFactory

pytestmark = pytest.mark.django_db


class TestPermissions:
    def test_card_owner(self, card):
        assert card.owner.has_perm("cards.view_card", card)
        assert card.owner.has_perm("cards.change_card", card)
        assert card.owner.has_perm("cards.delete_card", card)
        assert card.owner.has_perm("cards.move_card", card)

    def test_card_assignee(self, card):
        card = CardFactory(assignee=UserFactory())
        assert card.assignee.has_perm("cards.view_card", card)
        assert not card.assignee.has_perm("cards.change_card", card)
        assert not card.assignee.has_perm("cards.delete_card", card)
        assert card.assignee.has_perm("cards.move_card", card)

    def test_anonymous_user(self, anonymous_user, card, project):
        assert not anonymous_user.has_perm("cards.create_card", project)
        assert not anonymous_user.has_perm("cards.view_card", card)
        assert not anonymous_user.has_perm("cards.change_card", card)
        assert not anonymous_user.has_perm("cards.delete_card", card)
        assert not anonymous_user.has_perm("cards.move_card", card)

    def test_non_project_member(self, project):
        card = CardFactory(project=project)
        user = UserFactory()
        assert not user.has_perm("cards.create_card", project)
        assert not user.has_perm("cards.view_card", card)
        assert not user.has_perm("cards.change_card", card)
        assert not user.has_perm("cards.delete_card", card)
        assert not user.has_perm("cards.move_card", card)

    def test_project_member(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MEMBER)
        card = CardFactory(project=member.project)
        assert user.has_perm("cards.create_card", member.project)
        assert user.has_perm("cards.view_card", card)
        assert not user.has_perm("cards.change_card", card)
        assert not user.has_perm("cards.delete_card", card)
        assert not user.has_perm("cards.move_card", card)

    def test_project_manager(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MANAGER)
        card = CardFactory(project=member.project)
        assert user.has_perm("cards.create_card", member.project)
        assert user.has_perm("cards.view_card", card)
        assert user.has_perm("cards.change_card", card)
        assert user.has_perm("cards.delete_card", card)
        assert user.has_perm("cards.move_card", card)

    def test_project_admin(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.ADMIN)
        card = CardFactory(project=member.project)
        assert user.has_perm("cards.create_card", member.project)
        assert user.has_perm("cards.view_card", card)
        assert user.has_perm("cards.change_card", card)
        assert user.has_perm("cards.delete_card", card)
        assert user.has_perm("cards.move_card", card)

    def test_project_owner(self, project):
        card = CardFactory(project=project)
        assert project.owner.has_perm("cards.create_card", project)
        assert project.owner.has_perm("cards.view_card", card)
        assert project.owner.has_perm("cards.change_card", card)
        assert project.owner.has_perm("cards.delete_card", card)
        assert project.owner.has_perm("cards.move_card", card)
