# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

# Local
from .forms import ProjectCreationForm
from .models import Project


@login_required
def projects_overview(request):
    """Show all projects the user owns or belongs to"""
    projects = (
        Project.objects.accessible_to(request.user)
        .order_by("-created")
        .select_related("owner")
    )
    return TemplateResponse(request, "projects/overview.html", {"projects": projects})


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, _("Your project has been created"))
            return redirect("projects:projects_overview")
    else:
        form = ProjectCreationForm()
    return TemplateResponse(request, "projects/project_form.html", {"form": form})
