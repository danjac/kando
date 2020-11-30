# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

# Kando
from kando.cards.models import Card
from kando.users.utils import has_perm_or_403

# Local
from .forms import AttachmentForm
from .models import Attachment


@login_required
@require_POST
def create_attachment(request, card_id):
    # for now we just add attachments to cards
    card = get_object_or_404(
        Card.objects.select_related("owner", "project", "assignee"), pk=card_id
    )
    has_perm_or_403(request.user, "attachments.create_attachment", card)

    form = AttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        attachment = form.save(commit=False)
        attachment.card = card
        attachment.project = card.project
        attachment.owner = request.user
        attachment.save()
    return redirect(card)


@login_required
@require_POST
def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(
        Attachment.objects.select_related(
            "owner", "card", "card__project", "card__owner", "card__assignee"
        ),
        pk=attachment_id,
    )
    has_perm_or_403(request.user, "attachments.delete_attachment", attachment)
    attachment.delete()
    messages.info(request, _("Attachment has been deleted"))
    return redirect(attachment.card)
