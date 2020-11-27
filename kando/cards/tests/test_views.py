# Standard Library
import json

# Django
from django.urls import reverse

# Third Party Libraries
import pytest

# Kando
from kando.columns.factories import ColumnFactory
from kando.projects.factories import ProjectFactory

# Local
from ..factories import CardFactory
from ..models import Card

pytestmark = pytest.mark.django_db


class TestCreateCard:
    def test_get(self, client, login_user):
        project = ProjectFactory(owner=login_user)
        ColumnFactory.create_batch(3, project=project)
        response = client.get(reverse("cards:create_card", args=[project.id]))
        assert response.status_code == 200

    def test_post(self, client, login_user):
        project = ProjectFactory(owner=login_user)
        columns = ColumnFactory.create_batch(3, project=project)
        data = {
            "column": columns[0].id,
            "name": "test card",
            "description": "test desc",
            "priority": 1,
            "complexity": 1,
            "hours_estimated": 1,
        }
        response = client.post(reverse("cards:create_card", args=[project.id]), data)
        assert response.url == project.get_absolute_url()

        card = Card.objects.get()

        assert card.owner == login_user
        assert card.project == project
        assert card.column == columns[0]

    def test_get_for_column(self, client, login_user):
        project = ProjectFactory(owner=login_user)
        columns = ColumnFactory.create_batch(3, project=project)
        response = client.get(
            reverse("cards:create_card_for_column", args=[project.id, columns[0].id])
        )
        assert response.status_code == 200
        assert response.context["form"].initial["column"] == columns[0].id


class TestMoveCards:
    def test_post(self, client, login_user):
        project = ProjectFactory(owner=login_user)
        cards = CardFactory.create_batch(12, project=project)
        new_column = ColumnFactory(project=project)
        data = {"items": [card.id for card in cards]}
        response = client.post(
            reverse("cards:move_cards", args=[new_column.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 204
        assert Card.objects.filter(column=new_column).count() == 12

    def test_post_if_exceeds_limit(self, client, login_user):
        project = ProjectFactory(owner=login_user, task_limit=6)
        cards = CardFactory.create_batch(12, project=project)
        new_column = ColumnFactory(project=project)
        data = {"items": [card.id for card in cards]}
        response = client.post(
            reverse("cards:move_cards", args=[new_column.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert Card.objects.filter(column=new_column).count() == 0
