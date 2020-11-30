# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

# Kando
from kando.cards.models import Card
from kando.common.dragdrop import sort_draggable_items
from kando.common.http import HttpResponseNoContent
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

    for position, task in sort_draggable_items(
        request, card.task_set.all(), ["position"]
    ):
        task.position = position

    return HttpResponseNoContent()


@login_required
@require_POST
def edit_task(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related(
            "owner", "card", "card__project", "card__owner", "card__assignee"
        ),
        pk=task_id,
    )
    has_perm_or_403(request.user, "tasks.change_task", task)
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
    has_perm_or_403(request.user, "tasks.delete_task", task)
    task.delete()
    return redirect(task.card)


@login_required
@require_POST
def toggle_task_complete(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related("owner", "card", "card__owner", "card__assignee"),
        pk=task_id,
    )
    has_perm_or_403(request.user, "tasks.change_task", task)
    task.completed = None if task.completed else timezone.now()
    task.save()
    return redirect(task.card)
