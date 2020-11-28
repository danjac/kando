# Third Party Libraries
# Django
from django.conf import settings
from django.urls import reverse

import pytest

# Kando
from kando.projects.factories import ProjectMemberFactory
from kando.users.factories import UserFactory

# Local
from ..factories import InviteFactory

pytestmark = pytest.mark.django_db


class TestAcceptInvite:
    def test_accept_project_member(self, client, login_user):
        invite = InviteFactory(email=login_user.email)
        ProjectMemberFactory(project=invite.project, user=login_user)
        response = client.get(reverse("invites:accept_invite", args=[invite.pk]))
        assert response.url == invite.project.get_absolute_url()

        # tbd: invite model test
        invite.refresh_from_db()
        assert not invite.accepted

    def test_accept_existing_authenticated_user(self, client, login_user):
        invite = InviteFactory(email=login_user.email)
        response = client.get(reverse("invites:accept_invite", args=[invite.pk]))
        assert response.url == invite.project.get_absolute_url()
        assert login_user in invite.project.members.all()

        # tbd: invite model test
        invite.refresh_from_db()
        assert invite.accepted
        assert invite.invitee == login_user

    def test_accept_existing_unauthenticated_user(self, client):
        invite = InviteFactory(email=UserFactory().email)
        response = client.get(reverse("invites:accept_invite", args=[invite.pk]))
        assert response.url.startswith(reverse(settings.LOGIN_URL))

        invite.refresh_from_db()
        assert not invite.accepted

    def test_accept_new_user(self, client):
        invite = InviteFactory()
        response = client.get(reverse("invites:accept_invite", args=[invite.pk]))
        assert response.url.startswith(reverse("account_signup"))

        invite.refresh_from_db()
        assert not invite.accepted
