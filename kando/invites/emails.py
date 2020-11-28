# Django
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

# from django.utils.translation import override


def send_invite_email(invite):
    context = {"invite": invite, "project": invite.project, "accept_url": ""}
    send_mail(
        _("You have been invited to join our project!"),
        render_to_string("invites/emails/invite.txt", context),
        from_email="invites@localhost",
        recipient_list=[invite.email],
        html_message=render_to_string("invites/emails/invite.html", context),
    )
