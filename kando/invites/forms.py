# Django
from django import forms
from django.core.validators import validate_email
from django.utils.translation import gettext as _

# Local
from .models import Invite


class InviteForm(forms.Form):
    emails = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop("project")
        super().__init__(*args, **kwargs)

    def clean_emails(self):
        emails = [
            email
            for email in [
                email.strip().lower()
                for email in self.cleaned_data["emails"].split("\n")
            ]
        ]

        if not emails:
            raise forms.ValidationError(_("No emails provided"))

        for email in emails:
            try:
                validate_email(email)
            except forms.ValidationError as e:
                raise forms.ValidationError(
                    _("Email address %(email)s is invalid"), params={"email": email}
                ) from e

            if self.project.owner.email == email:
                raise forms.ValidationError(
                    _("Email address %(email)s is already a member of this project"),
                    params={"email": email},
                )

        invites = self.project.invite_set.filter(email__in=emails).iterator()

        for invite in invites:
            if invite.email in emails:
                raise forms.ValidationError(
                    _(
                        "Email address %(email)s has already been invited to this project"
                    ),
                    params={"email": invite.email},
                )

        members = self.project.members.filter(email__in=emails).iterator()

        for member in members:
            if member.email in emails:
                raise forms.ValidationError(
                    _("Email address %(email)s is already a member of this project"),
                    params={"email": member.email},
                )

        return emails

    def save(self, sender):
        invites = [
            Invite(sender=sender, project=self.project, email=email)
            for email in self.cleaned_data["emails"]
        ]
        return Invite.objects.bulk_create(invites)
