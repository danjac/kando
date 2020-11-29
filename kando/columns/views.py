# Standard Library
import json

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

# Kando
from kando.projects.models import Project
from kando.users.utils import has_perm_or_403

# Local
from .forms import ColumnForm
from .models import Column


@login_required
def create_column(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "columns.create_column", project)
    if request.method == "POST":
        form = ColumnForm(request.POST)
        if form.is_valid():
            column = form.save(commit=False)
            column.project = project
            column.save()
            messages.success(request, _("Column has been added"))
            return redirect(project)
    else:
        form = ColumnForm()
    return TemplateResponse(
        request, "columns/column_form.html", {"form": form, "project": project}
    )


@login_required
def edit_column(request, column_id):
    column = get_object_or_404(
        Column.objects.select_related("project", "project__owner"), pk=column_id
    )
    has_perm_or_403(request.user, "columns.change_column", column)
    if request.method == "POST":
        form = ColumnForm(request.POST, instance=column)
        if form.is_valid():
            form.save()
            messages.success(request, _("Column has been updated"))
            return redirect(column.project)
    else:
        form = ColumnForm()
    return TemplateResponse(
        request,
        "columns/column_form.html",
        {"form": form, "project": column.project, "column": column},
    )


@login_required
@require_POST
def delete_column(request, column_id):
    column = get_object_or_404(
        Column.objects.select_related("project", "project__owner"), pk=column_id
    )
    has_perm_or_403(request.user, "columns.delete_column", column)
    if column.card_set.count() > 0:
        messages.error(request, _("You cannot delete a column containing cards"))
    else:
        column.delete()
        messages.info(request, _("Column has been deleted"))
    return redirect(column.project)


@login_required
def move_columns(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)

    try:
        column_ids = [int(pk) for pk in json.loads(request.body)["items"]]
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Invalid payload")

    qs = project.column_set.all()
    columns = qs.in_bulk()
    for_update = []

    for position, column_id in enumerate(column_ids, 1):
        column = columns.get(column_id)
        if column:
            column.position = position
            for_update.append(column)

    qs.bulk_update(for_update, ["position"])
    return HttpResponse(status=204)
