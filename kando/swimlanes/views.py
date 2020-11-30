# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

# Kando
from kando.projects.models import Project
from kando.users.utils import has_perm_or_403

# Local
from .forms import SwimlaneForm


@login_required
def create_swimlane(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "swimlanes.create_swimlane", project)
    if request.method == "POST":
        form = SwimlaneForm(request.POST)
        if form.is_valid():
            swimlane = form.save(commit=False)
            swimlane.project = project
            swimlane.save()
            messages.success(request, _("Swimlane has been added"))
            return redirect(project)
    else:
        form = SwimlaneForm()
    return TemplateResponse(
        request, "swimlanes/swimlane_form.html", {"form": form, "project": project}
    )
