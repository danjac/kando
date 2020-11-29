# Third Party Libraries
import pytest

# Kando
from kando.cards.factories import CardFactory
from kando.tasks.factories import TaskFactory
from kando.users.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestPermissions:
    def test_card_owner(self, task):
        assert task.card.owner.has_perm("tasks.create_task", task.card)
        assert task.card.owner.has_perm("tasks.move_tasks", task.card)
        assert task.card.owner.has_perm("tasks.change_task", task)
        assert task.card.owner.has_perm("tasks.delete_task", task)

    def test_card_assignee(self):
        user = UserFactory()
        card = CardFactory(assignee=user)
        task = TaskFactory(card=card)
        assert card.assignee.has_perm("tasks.create_task", card)
        assert card.assignee.has_perm("tasks.move_tasks", card)
        assert card.assignee.has_perm("tasks.change_task", task)
        assert card.assignee.has_perm("tasks.delete_task", task)
