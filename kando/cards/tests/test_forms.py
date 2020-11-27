# Kando
# Third Party Libraries
import pytest

from kando.columns.factories import ColumnFactory
from kando.projects.factories import ProjectFactory

# Local
from ..factories import CardFactory
from ..forms import CardForm

pytestmark = pytest.mark.django_db


class TestCardForm:
    def test_is_valid(self, project):
        columns = ColumnFactory.create_batch(4, project=project)
        data = {
            "column": columns[0].id,
            "name": "test card",
            "description": "test desc",
            "priority": 1,
            "complexity": 1,
            "hours_estimated": 1,
        }
        form = CardForm(data, project=project)
        assert form.is_valid()

    def test_exceeds_task_limit(self):
        project = ProjectFactory(task_limit=1)
        columns = ColumnFactory.create_batch(4, project=project)
        CardFactory(project=project, column=columns[0])
        data = {
            "column": columns[0].id,
            "name": "test card",
            "description": "test desc",
            "priority": 1,
            "complexity": 1,
            "hours_estimated": 1,
        }
        form = CardForm(data, project=project)
        assert not form.is_valid()
