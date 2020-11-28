# Third Party Libraries
import rules

# Kando
from kando.cards.rules import is_card_owner_or_assignee

rules.add_perm("tasks.create_task", is_card_owner_or_assignee)
rules.add_perm("tasks.update_task", is_card_owner_or_assignee)
rules.add_perm("tasks.delete_task", is_card_owner_or_assignee)
rules.add_perm("tasks.move_task", is_card_owner_or_assignee)
