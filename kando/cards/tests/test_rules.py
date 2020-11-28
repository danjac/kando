# Third Party Libraries
import pytest

# Kando
from kando.projects.factories import ProjectMemberFactory
from kando.projects.models import ProjectMember

# Local
from ..factories import CardFactory

pytestmark = pytest.mark.django_db


class TestPermissions:
    def test_project_owner(self, card):
        assert card.owner.has_perm("cards.view_card", card)
        assert card.owner.has_perm("cards.change_card", card)
        assert card.owner.has_perm("cards.delete_card", card)

    def test_anonymous_user(self, anonymous_user, card):
        assert not anonymous_user.has_perm("cards.view_card", card)
        assert not anonymous_user.has_perm("cards.change_card", card)
        assert not anonymous_user.has_perm("cards.delete_card", card)

    def test_non_member(self, user):
        card = CardFactory()
        assert not user.has_perm("cards.view_card", card)
        assert not user.has_perm("cards.change_card", card)
        assert not user.has_perm("cards.delete_card", card)

    def test_member(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MEMBER)
        card = CardFactory(project=member.project)
        assert user.has_perm("cards.view_card", card)
        assert not user.has_perm("cards.change_card", card)
        assert not user.has_perm("cards.delete_card", card)

    def test_manager(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.MANAGER)
        card = CardFactory(project=member.project)
        assert user.has_perm("cards.view_card", card)
        assert user.has_perm("cards.change_card", card)
        assert user.has_perm("cards.delete_card", card)

    def test_admin(self, user):
        member = ProjectMemberFactory(user=user, role=ProjectMember.Role.ADMIN)
        card = CardFactory(project=member.project)
        assert user.has_perm("cards.view_card", card)
        assert user.has_perm("cards.change_card", card)
        assert user.has_perm("cards.delete_card", card)