# Third Party Libraries
# Standard Library
import json

# Django
from django.urls import reverse
from django.utils import timezone

import pytest

# Kando
from kando.cards.factories import CardFactory
from kando.projects.factories import ProjectFactory
from kando.tasks.factories import TaskFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def project_for_login_user(login_user):
    return ProjectFactory(owner=login_user)


@pytest.fixture
def card_for_login_user(project_for_login_user):
    return CardFactory(
        project=project_for_login_user, owner=project_for_login_user.owner
    )


@pytest.fixture
def task_for_login_user(card_for_login_user):
    return TaskFactory(card=card_for_login_user)


class TestCreateTask:
    def test_post(self, client, card_for_login_user):
        data = {"description": "test"}
        response = client.post(
            reverse("tasks:create_task", args=[card_for_login_user.id]), data
        )
        assert response.url == card_for_login_user.get_absolute_url()
        task = card_for_login_user.task_set.first()
        assert task.owner == card_for_login_user.owner
        assert task.card == card_for_login_user


class TestEditTask:
    def test_post(self, client, task_for_login_user):
        data = {"description": "test"}
        response = client.post(
            reverse("tasks:edit_task", args=[task_for_login_user.id]), data
        )
        assert response.url == task_for_login_user.card.get_absolute_url()
        task_for_login_user.refresh_from_db()
        assert task_for_login_user.description == "test"


class TestDeleteTask:
    def test_post(self, client, task_for_login_user):
        response = client.post(
            reverse("tasks:delete_task", args=[task_for_login_user.id]),
        )
        assert response.url == task_for_login_user.card.get_absolute_url()
        assert task_for_login_user.card.task_set.count() == 0


class TestToggleTaskComplete:
    def test_post_not_complete(self, client, task_for_login_user):
        response = client.post(
            reverse("tasks:toggle_complete", args=[task_for_login_user.id]),
        )
        assert response.url == task_for_login_user.card.get_absolute_url()
        task_for_login_user.refresh_from_db()
        assert task_for_login_user.completed

    def test_post_complete(self, client, card_for_login_user):
        task = TaskFactory(card=card_for_login_user, completed=timezone.now())
        response = client.post(reverse("tasks:toggle_complete", args=[task.id]),)
        assert response.url == card_for_login_user.get_absolute_url()
        task.refresh_from_db()
        assert not task.completed


class TestMoveTasks:
    def test_post(self, client, card_for_login_user):
        tasks = TaskFactory.create_batch(12, card=card_for_login_user)
        data = {"items": [task.id for task in tasks]}
        response = client.post(
            reverse("tasks:move_tasks", args=[card_for_login_user.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 204
