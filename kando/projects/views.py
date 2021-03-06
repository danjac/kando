# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

# Kando
from kando.attachments.models import Attachment
from kando.cards.models import Card
from kando.tasks.models import Task
from kando.users.utils import has_perm_or_403, user_display

# Local
from .forms import ProjectCreationForm, ProjectForm, ProjectMemberRoleForm
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

    breadcrumbs = [
        (_("Projects"), reverse("projects:projects_overview")),
        (_("New Project"), None),
    ]

    return TemplateResponse(
        request,
        "projects/project_form.html",
        {"form": form, "breadcrumbs": breadcrumbs},
    )


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

    breadcrumbs = [
        (_("Projects"), reverse("projects:projects_overview")),
        (project.name, project.get_absolute_url()),
        (_("Edit Project"), None),
    ]

    return TemplateResponse(
        request,
        "projects/project_form.html",
        {"form": form, "project": project, "breadcrumbs": breadcrumbs},
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
@require_POST
def duplicate_project(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "projects.view_project", project)

    duplicate = Project.objects.create(
        name=f"[DUPLICATE] {project.name}", owner=request.user,
    )

    for column in project.column_set.all():
        duplicate.column_set.create(name=column.name, position=column.position)

    messages.success(request, _("New project created"))
    return redirect(duplicate)


@login_required
def project_board(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "projects.view_project", project)

    columns = project.column_set.order_by("position")

    cards = project.card_set.order_by("position").select_related(
        "project", "owner", "column", "assignee",
    )

    breadcrumbs = [
        (_("Projects"), reverse("projects:projects_overview")),
        (project.name, None),
    ]

    return TemplateResponse(
        request,
        "projects/board.html",
        {
            "project": project,
            "columns": columns,
            "cards": cards,
            "breadcrumbs": breadcrumbs,
        },
    )


@login_required
def project_members(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "projects.view_project", project)

    members = project.projectmember_set.select_related("user", "project").order_by(
        "user__name", "user__username"
    )
    breadcrumbs = [
        (_("Projects"), reverse("projects:projects_overview")),
        (project.name, project.get_absolute_url()),
        (_("Users and Permissions"), None),
    ]

    return TemplateResponse(
        request,
        "projects/members.html",
        {"project": project, "members": members, "breadcrumbs": breadcrumbs},
    )


@login_required
@require_POST
def change_member_role(request, member_id):
    member = get_object_or_404(
        ProjectMember.objects.select_related("user", "project", "project__owner"),
        pk=member_id,
    )
    has_perm_or_403(request.user, "projects.change_member_role", member)

    form = ProjectMemberRoleForm(request.POST, instance=member)
    if form.is_valid():
        member = form.save()
        messages.success(
            request,
            _("Member %(name)s has been updated to %(role)s")
            % {"name": member.user.username, "role": member.get_role_display()},
        )

    return redirect("projects:member_detail", member.project.id, member.user.username)


@login_required
@require_POST
def remove_member(request, member_id):
    member = get_object_or_404(
        ProjectMember.objects.select_related("user", "project", "project__owner"),
        pk=member_id,
    )
    has_perm_or_403(request.user, "projects.remove_member", member)

    with transaction.atomic():

        # transfer ownership of cards, tasks, and attachments to project owner
        Card.objects.filter(owner=member.user, project=member.project).update(
            owner=member.project.owner
        )

        Card.objects.filter(assignee=member.user, project=member.project).update(
            assignee=None
        )

        Task.objects.filter(owner=member.user, card__project=member.project).update(
            owner=member.project.owner
        )

        Attachment.objects.filter(owner=member.user, project=member.project).update(
            owner=member.project.owner
        )

        member.delete()

    messages.info(
        request,
        _("Member %(name)s has been removed from this project")
        % {"name": member.user.username,},
    )

    return redirect("projects:project_members", member.project.id)


@login_required
def project_member_detail(request, project_id, username):

    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)

    has_perm_or_403(request.user, "projects.view_project", project)

    if project.owner.username == username:
        is_owner = True
        member = None
        user = project.owner
        member_role_form = None
    else:
        member = get_object_or_404(
            ProjectMember.objects.select_related("project", "user", "project__owner"),
            user__username=username,
            project=project,
        )
        is_owner = False
        user = member.user
        member_role_form = ProjectMemberRoleForm(instance=member)

    if not is_owner and not member:
        raise Http404()

    cards = project.card_set.order_by("-priority", "-created").select_related(
        "project", "column", "owner", "assignee"
    )

    owned_cards = cards.filter(owner=user)
    assigned_cards = cards.filter(assignee=user)

    breadcrumbs = [
        (_("Projects"), reverse("projects:projects_overview")),
        (project.name, project.get_absolute_url()),
        (
            _("Users and Permissions"),
            reverse("projects:project_members", args=[project.id]),
        ),
        (user_display(user), None),
    ]

    return TemplateResponse(
        request,
        "projects/member_detail.html",
        {
            "project": project,
            "user_obj": user,
            "member": member,
            "member_role_form": member_role_form,
            "is_owner": is_owner,
            "owned_cards": owned_cards,
            "assigned_cards": assigned_cards,
            "breadcrumbs": breadcrumbs,
        },
    )
