# Standard Library
import json

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

# Kando
from kando.columns.models import Column
from kando.projects.models import Project

# Local
from .forms import CardForm
from .models import Card


@login_required
def create_card(request, project_id, column_id=None):

    # for now, only owner can create card.
    project = get_object_or_404(
        Project.objects.accessible_to(request.user), pk=project_id
    )

    if request.method == "POST":
        form = CardForm(request.POST, project=project)
        if form.is_valid():
            card = form.save(commit=False)
            card.owner = request.user
            card.project = project
            # tbd: tidy this up later
            card.position = (
                card.column.card_set.aggregate(Max("position"))["position__max"] or 0
            ) + 1
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
        Card.objects.accessible_to(request.user).select_related("project", "column"),
        pk=card_id,
    )
    return TemplateResponse(request, "cards/detail.html", {"card": card})


@login_required
def edit_card(request, card_id):
    card = get_object_or_404(
        Card.objects.accessible_to(request.user).select_related("project"), pk=card_id,
    )
    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, _("Card has been updated"))
            return redirect(card)
    else:
        form = CardForm(instance=card)

    return TemplateResponse(
        request, "cards/card_form.html", {"card": card, "form": form}
    )


@login_required
@require_POST
def delete_card(request, card_id):
    card = get_object_or_404(
        Card.objects.accessible_to(request.user).select_related("project"), pk=card_id,
    )
    card.delete()
    messages.info(request, _("Card has been deleted"))
    return redirect(card.project)


@login_required
@require_POST
def move_cards(request, column_id):
    # for now only owner can move cards
    column = get_object_or_404(
        Column.objects.filter(project__owner=request.user).select_related("project"),
        pk=column_id,
    )

    try:
        card_ids = [int(pk) for pk in json.loads(request.body)["items"]]
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Invalid payload")

    if column.project.task_limit and len(card_ids) > column.project.task_limit:
        return HttpResponseBadRequest("Exceeds project task limit")

    qs = column.project.card_set.all()
    cards = qs.in_bulk()
    for_update = []
    for position, card_id in enumerate(card_ids, 1):
        card = cards.get(card_id)
        if card:
            card.position = position
            card.column_id = column_id
            for_update.append(card)
    qs.bulk_update(for_update, ["position", "column"])
    return HttpResponse(status=204)
