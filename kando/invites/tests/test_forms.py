# Third Party Libraries
import pytest

# Kando
from kando.projects.factories import ProjectMemberFactory
from kando.users.factories import UserFactory

# Local
from ..factories import InviteFactory
from ..forms import InviteForm

pytestmark = pytest.mark.django_db


class TestInviteForm:
    def test_already_invited_email_other_project(self, project):
        InviteFactory(email="example1@example.com")
        data = {
            "emails": """
            example1@example.com
            example2@example.com
            """
        }
        form = InviteForm(data, project=project)
        assert form.is_valid()

    def test_already_invited_email_same_project(self, project):
        InviteFactory(email="example1@example.com", project=project)
        data = {
            "emails": """
            example1@example.com
            example2@example.com
            """
        }
        form = InviteForm(data, project=project)
        assert not form.is_valid()

    def test_invalid_email(self, project):
        data = {
            "emails": """
            example1.example.com
            example2@example.com
            """
        }
        form = InviteForm(data, project=project)
        assert not form.is_valid()

    def test_project_owner_email(self, project):
        data = {
            "emails": f"""
            {project.owner.email}
            example2@example.com
            """
        }
        form = InviteForm(data, project=project)
        assert not form.is_valid()

    def test_project_member_email(self, project):
        member = ProjectMemberFactory(project=project)
        data = {
            "emails": f"""
            {member.user.email}
            example2@example.com
            """
        }
        form = InviteForm(data, project=project)
        assert not form.is_valid()

    def test_save(self, project):
        # one new user and one existing user
        UserFactory(email="example1@example.com")
        data = {
            "emails": """
            example1@example.com
            example2@example.com
            """
        }
        form = InviteForm(data, project=project)
        assert form.is_valid()
        invites = form.save(project.owner)
        assert len(invites) == 2
