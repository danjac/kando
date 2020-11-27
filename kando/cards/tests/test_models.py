# Third Party Libraries
import pytest

# Kando
from kando.projects.factories import ProjectMemberFactory
from kando.users.factories import UserFactory

# Local
from ..factories import CardFactory
from ..models import Card

pytestmark = pytest.mark.django_db


class TestCardManager:
    def test_accessible_to_if_owner(self, card):
        assert Card.objects.accessible_to(card.project.owner).count() == 1

    def test_accessible_to_if_not_owner(self, card):
        assert Card.objects.accessible_to(UserFactory()).count() == 0

    def test_accessible_to_if_member(self, user):
        member = ProjectMemberFactory(user=user)
        CardFactory(project=member.project)
        assert Card.objects.accessible_to(user).count() == 1

    def test_accessible_to_if_inactive_member(self, user):
        member = ProjectMemberFactory(user=user, is_active=False)
        CardFactory(project=member.project)
        assert Card.objects.accessible_to(user).count() == 0
