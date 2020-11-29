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


class TestCardModel:
    def test_position_if_new_card(self, column):
        card = CardFactory(column=column)
        assert card.position == 1

    def test_position_if_already_another_card(self, column):
        CardFactory(column=column)

        card = CardFactory(column=column)
        assert card.position == 2

    def test_position_if_column_changed(self, column):

        CardFactory(column=column)

        card = CardFactory()
        assert card.position == 1

        card.column = column
        card.save()
        assert card.position == 2
