# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

# Kando
from kando.projects.models import Project

# Local
from .forms import CardForm


@login_required
def create_card(request, project_id, column_id=None):

    # for now, only owner can create card.
    project = get_object_or_404(Project, owner=request.user, pk=project_id)

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
            return redirect("projects:project_board", project.id)
    else:
        form = CardForm(initial={"column": column_id}, project=project)
    return TemplateResponse(
        request, "cards/card_form.html", {"form": form, "project": project}
    )
