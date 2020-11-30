# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

# Kando
from kando.users.utils import has_perm_or_403

# Local
from .forms import ProjectCreationForm, ProjectForm
from .models import Project, ProjectMember


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
            project = form.save(request.user)
            messages.success(request, _("Your project has been created"))
            return redirect(project)
    else:
        form = ProjectCreationForm()
    return TemplateResponse(request, "projects/project_form.html", {"form": form})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "projects.change_project", project)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your project has been updated"))
            return redirect(project)
    else:
        form = ProjectForm(instance=project)
    return TemplateResponse(
        request, "projects/project_form.html", {"form": form, "project": project}
    )


@login_required
@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "projects.delete_project", project)

    project.delete()
    messages.info(request, _("Your project has been deleted"))
    return redirect("projects:projects_overview")


@login_required
def project_board(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "projects.view_project", project)

    columns = project.column_set.order_by("position")
    swimlanes = project.swimlane_set.order_by("position")

    cards = project.card_set.order_by("position").select_related(
        "project", "owner", "column", "assignee", "swimlane"
    )

    return TemplateResponse(
        request,
        "projects/board.html",
        {
            "project": project,
            "columns": columns,
            "swimlanes": swimlanes,
            "cards": cards,
        },
    )


@login_required
def project_members(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "projects.view_project", project)

    members = project.projectmember_set.select_related("user", "project").order_by(
        "user__name", "user__username"
    )

    return TemplateResponse(
        request, "projects/members.html", {"project": project, "members": members}
    )


@login_required
def project_member_detail(request, project_id, username):

    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)

    has_perm_or_403(request.user, "projects.view_project", project)

    if project.owner.username == username:
        is_owner = True
        member = None
        user = project.owner
    else:
        member = (
            ProjectMember.objects.select_related("project", "user", "project__owner")
            .filter(user__username__iexact=username, project=project)
            .first()
        )
        is_owner = False
        user = member.user

    if not is_owner and not member:
        raise Http404()

    cards = project.card_set.order_by("-priority", "-created").select_related(
        "project", "column", "owner", "assignee"
    )

    owned_cards = cards.filter(owner=user)
    assigned_cards = cards.filter(assignee=user)

    return TemplateResponse(
        request,
        "projects/member_detail.html",
        {
            "project": project,
            "user_obj": user,
            "member": member,
            "is_owner": is_owner,
            "owned_cards": owned_cards,
            "assigned_cards": assigned_cards,
        },
    )
