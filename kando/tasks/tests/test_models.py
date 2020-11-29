# Third Party Libraries
import pytest

# Kando
from kando.tasks.factories import TaskFactory

pytestmark = pytest.mark.django_db


class TestTaskModel:
    def test_position_if_new_task(self, card):
        task = TaskFactory(card=card)
        assert task.position == 1

    def test_position_if_already_another_task(self, card):
        TaskFactory(card=card)

        task = TaskFactory(card=card)
        assert task.position == 2
