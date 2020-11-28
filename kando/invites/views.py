# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.functional import gettext as _

# Kando
from kando.projects.models import Project
from kando.users.utils import has_perm_or_403

# Local
from .forms import ProjectInviteForm
from .models import Invite


@login_required
def invite_users(request, project_id):
    project = get_object_or_404(Project.objects.select_related("owner"), pk=project_id)
    has_perm_or_403(request.user, "projects.manage_users", project)

    if request.method == "POST":
        form = ProjectInviteForm(request.POST, project=project)
        if form.is_valid():
            invites = form.save()
            messages.success(
                _("You have sent %(num_invites)s invites")
                % {"num_invites": len(invites)}
            )
            return redirect("projects:project_members", project.id)
    else:
        form = ProjectInviteForm(project=project)
    return TemplateResponse(
        request, "projects/invite_form.html", {"form": form, "project": project}
    )


def accept_invite(request, invite_id):
    invite = get_object_or_404(
        Invite.objects.filter(accepted__isnull=True).select_related("project", "user"),
        pk=invite_id,
    )

    # if user exists with this email, check if user logged in, redirect to
    # login otherwise

    user = get_user_model().objects.for_email(invite.email).first()

    if user and request.user.is_authenticated:
        if request.user == user:
            invite.accept(request.user)
            messages.success(request, _("You have joined this project"))
            return redirect(invite.project)
        else:
            # prevent deliberate or accidental hijack of invite
            raise Http404(_("This invite is invalid"))

    if user:
        # if user not logged in, log in first and redirect back here to accept invitation
        login_url = settings.LOGIN_URL
        message = _("Please log in to join this project")

    else:
        # user not in system yet, signup first
        login_url = reverse("account_signup")
        message = _("Please register first before joining this project")

    messages.info(request, message)

    return redirect_to_login(request.path, login_url, REDIRECT_FIELD_NAME)
