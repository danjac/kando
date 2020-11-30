# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

# Kando
from kando.columns.models import Column
from kando.common.utils import sort_draggable_items
from kando.projects.models import Project
from kando.users.utils import has_perm_or_403

# Local
from .forms import CardForm
from .models import Card


@login_required
def create_card(request, project_id, column_id=None):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "cards.create_card", project)

    if request.method == "POST":
        form = CardForm(request.POST, project=project)
        if form.is_valid():
            card = form.save(commit=False)
            card.owner = request.user
            card.project = project
            card.save()
            messages.success(request, _("Your card has been added"))
            return redirect(card)
    else:
        form = CardForm(initial={"column": column_id}, project=project)
    return TemplateResponse(
        request, "cards/card_form.html", {"form": form, "project": project}
    )


@login_required
def card_detail(request, card_id):
    card = get_object_or_404(
        Card.objects.select_related(
            "project", "column", "project__owner", "assignee", "owner"
        ),
        pk=card_id,
    )
    has_perm_or_403(request.user, "cards.view_card", card)

    tasks = card.task_set.select_related(
        "card", "owner", "card__owner", "card__assignee"
    ).order_by("position")

    attachments = card.attachment_set.select_related(
        "card", "owner", "card__owner", "card__assignee"
    ).order_by("created")

    return TemplateResponse(
        request,
        "cards/detail.html",
        {"card": card, "tasks": tasks, "attachments": attachments},
    )


@login_required
def edit_card(request, card_id):
    card = get_object_or_404(
        Card.objects.select_related("project", "project__owner", "owner"), pk=card_id,
    )
    has_perm_or_403(request.user, "cards.change_card", card)
    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, _("Card has been updated"))
            return redirect(card)
    else:
        form = CardForm(instance=card)

    return TemplateResponse(
        request,
        "cards/card_form.html",
        {"card": card, "form": form, "project": card.project},
    )


@login_required
@require_POST
def delete_card(request, card_id):
    card = get_object_or_404(
        Card.objects.select_related("project", "project__owner"), pk=card_id,
    )
    has_perm_or_403(request.user, "cards.delete_card", card)
    card.delete()
    messages.info(request, _("Card has been deleted"))
    return redirect(card.project)


@login_required
@require_POST
def move_cards(request, column_id):
    column = get_object_or_404(Column.objects.select_related("project"), pk=column_id)

    qs = column.project.card_set.select_related(
        "project", "project__owner", "assignee", "owner"
    )

    for position, card in sort_draggable_items(request, qs, ["position", "column"]):
        has_perm_or_403(request.user, "cards.move_card", card)
        card.position = position
        card.column_id = column_id

    return HttpResponse(status=204)
