# Standard Library
import json

# Django
from django.urls import reverse

# Third Party Libraries
import pytest

# Kando
from kando.cards.factories import CardFactory
from kando.projects.factories import ProjectFactory

# Local
from ..factories import ColumnFactory
from ..models import Column

pytestmark = pytest.mark.django_db


@pytest.fixture
def column_for_login_user(login_user):
    return ColumnFactory(project=ProjectFactory(owner=login_user))


class TestCreateColumn:
    def test_get(self, client, login_user):
        project = ProjectFactory(owner=login_user)
        response = client.get(reverse("columns:create_column", args=[project.id]))
        assert response.status_code == 200

    def test_post(self, client, login_user):
        project = ProjectFactory(owner=login_user)
        data = {"name": "test"}
        response = client.post(
            reverse("columns:create_column", args=[project.id]), data
        )
        assert response.url == project.get_absolute_url()
        assert project.column_set.count() == 1


class TestMoveColumns:
    def test_post(self, client, login_user):
        project = ProjectFactory(owner=login_user)
        first = ColumnFactory(project=project)
        second = ColumnFactory(project=project)

        assert first.position == 1
        assert second.position == 2

        data = {"items": [second.id, first.id]}

        response = client.post(
            reverse("columns:create_column", args=[project.id]), data
        )

        response = client.post(
            reverse("columns:move_columns", args=[project.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 204

        first.refresh_from_db()
        second.refresh_from_db()

        assert first.position == 2
        assert second.position == 1


class TestColumnDetail:
    def test_get(self, client, column_for_login_user):
        response = client.get(
            reverse("columns:column_detail", args=[column_for_login_user.id])
        )
        assert response.status_code == 200


class TestEditColumn:
    def test_get(self, client, column_for_login_user):
        response = client.get(
            reverse("columns:edit_column", args=[column_for_login_user.id])
        )
        assert response.status_code == 200

    def test_post(self, client, column_for_login_user):
        data = {"name": "test"}
        response = client.post(
            reverse("columns:edit_column", args=[column_for_login_user.id]), data
        )
        assert response.url == column_for_login_user.get_absolute_url()
        column_for_login_user.refresh_from_db()
        assert column_for_login_user.name == "test"


class TestDeleteColumn:
    def test_post(self, client, column_for_login_user):
        response = client.post(
            reverse("columns:delete_column", args=[column_for_login_user.id]),
        )
        assert response.url == column_for_login_user.project.get_absolute_url()
        assert Column.objects.count() == 0

    def test_post_with_cards(self, client, column_for_login_user):
        CardFactory(column=column_for_login_user)
        response = client.post(
            reverse("columns:delete_column", args=[column_for_login_user.id]),
        )
        assert response.url == column_for_login_user.project.get_absolute_url()
        assert Column.objects.count() == 1
