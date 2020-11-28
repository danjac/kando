# Third Party Libraries
import pytest

# Kando
from kando.projects.factories import ProjectMemberFactory
from kando.users.factories import UserFactory

# Local
from ..models import Invite

pytestmark = pytest.mark.django_db


class TestInviteModel:
    def test_accept(self, invite):
        user = UserFactory(email=invite.email)
        invite.accept(user)
        assert invite.invitee == user
        assert invite.accepted

    def test_accept_existing_member(self, invite):
        user = UserFactory(email=invite.email)
        ProjectMemberFactory(project=invite.project, user=user)
        with pytest.raises(Invite.AlreadyMember):
            invite.accept(user)
            assert not invite.invitee
            assert not invite.accepted
