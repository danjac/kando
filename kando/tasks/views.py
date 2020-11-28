# Django
from django.contrib import messages
from django.contrib.auth import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

# Kando
from kando.cards.models import Card
from kando.users.utils import has_perm_or_403

# Local
from .forms import TaskCreationForm


@login_required
def create_tasks(request, card_id):
    card = get_object_or_404(
        Card.objects.select_related("owner", "project", "assignee"), pk=card_id
    )
    has_perm_or_403(request.user, "tasks.create_task", card)

    if request.method == "POST":
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            tasks = form.save(request.user)
            messages.success(
                request, _("%(num_tasks)s added") % {"num_tasks": len(tasks)}
            )
            return redirect(card)
    else:
        form = TaskCreationForm()
    return TemplateResponse(
        request, "tasks/add_tasks.html", {"form": form, "card": card}
    )
