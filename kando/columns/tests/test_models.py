# Third Party Libraries
import pytest

# Local
from ..factories import ColumnFactory

pytestmark = pytest.mark.django_db


class TestColumnModel:
    def test_default_position(self):
        first = ColumnFactory()
        assert first.position == 1
        # same project
        second = ColumnFactory(project=first.project)
        assert second.position == 2
        # different project
        third = ColumnFactory()
        assert third.position == 1
