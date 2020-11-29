# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

# Kando
from kando.cards.models import Card
from kando.users.utils import has_perm_or_403

# Local
from .forms import TaskForm
from .models import Task


@login_required
def create_task(request, card_id):
    card = get_object_or_404(
        Card.objects.select_related("owner", "project", "assignee"), pk=card_id
    )
    has_perm_or_403(request.user, "tasks.create_task", card)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.card = card
            task.owner = request.user
            task.save()

            messages.success(request, _("Task has been added"))
            return redirect(card)
    else:
        form = TaskForm()
    return TemplateResponse(
        request, "tasks/task_form.html", {"form": form, "card": card}
    )


@login_required
@require_POST
def mark_complete(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related("owner", "project", "card"), pk=task_id
    )
    has_perm_or_403(request.user, "tasks.mark_complete", task)
    task.completed = timezone.now()
    task.save()
    return HttpResponse(status=204)


@login_required
@require_POST
def mark_uncomplete(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related("owner", "project", "card"), pk=task_id
    )
    has_perm_or_403(request.user, "tasks.mark_complete", task)
    task.completed = None
    task.save()
    return HttpResponse(status=204)
