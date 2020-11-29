# Kando
# Third Party Libraries
import pytest

from kando.columns.factories import ColumnFactory

# Local
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
