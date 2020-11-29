# Standard Library
import json

# Django
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

# Kando
from kando.cards.models import Card
from kando.users.utils import has_perm_or_403

# Local
from .forms import TaskForm
from .models import Task


@login_required
@require_POST
def create_task(request, card_id):
    card = get_object_or_404(
        Card.objects.select_related("owner", "project", "assignee"), pk=card_id
    )
    has_perm_or_403(request.user, "tasks.create_task", card)

    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.card = card
        task.owner = request.user
        task.save()
    return redirect(card)


@login_required
@require_POST
def move_tasks(request, card_id):
    card = get_object_or_404(
        Card.objects.select_related("owner", "project", "assignee"), pk=card_id
    )
    has_perm_or_403(request.user, "tasks.move_tasks", card)
    try:
        task_ids = [int(pk) for pk in json.loads(request.body)["items"]]
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Invalid payload")

    qs = card.task_set.all()
    tasks = qs.in_bulk()
    for_update = []

    for position, task_id in enumerate(task_ids, 1):
        task = tasks.get(task_id)
        if task:
            task.position = position
            for_update.append(task)

    qs.bulk_update(for_update, ["position"])
    return HttpResponse(status=204)


@login_required
@require_POST
def edit_task(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related(
            "owner", "card", "card__project", "card__owner", "card__assignee"
        ),
        pk=task_id,
    )
    # has_perm_or_403(request.user, "tasks.mark_complete", task)
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        task.save()
    return redirect(task.card)


@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related(
            "owner", "card", "card__project", "card__owner", "card__assignee"
        ),
        pk=task_id,
    )
    # has_perm_or_403(request.user, "tasks.mark_complete", task)
    task.delete()
    return redirect(task.card)


@login_required
@require_POST
def toggle_complete(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related("owner", "card", "card__owner", "card__assignee"),
        pk=task_id,
    )
    has_perm_or_403(request.user, "tasks.change_task", task)
    task.completed = None if task.completed else timezone.now()
    task.save()
    return redirect(task.card)
