# Third Party Libraries
import rules

# Kando
from kando.cards.rules import is_card_owner_or_assignee


@rules.predicate
def is_attachment_card_owner_or_assignee(user, attachment):
    return user.is_authenticated and is_card_owner_or_assignee(user, attachment.card)


rules.add_perm("attachments.create_attachment", is_card_owner_or_assignee)
rules.add_perm("attachments.delete_attachment", is_attachment_card_owner_or_assignee)
