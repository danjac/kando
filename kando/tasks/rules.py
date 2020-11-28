# Third Party Libraries
import rules

# Kando
from kando.cards.rules import is_card_owner_or_assignee


@rules.predicate
def is_task_owner(user, task):
    return user.is_authenticated and task.owner == user


rules.add_perm("tasks.create_task", is_card_owner_or_assignee)
rules.add_perm("tasks.update_task", is_card_owner_or_assignee)
rules.add_perm("tasks.delete_task", is_card_owner_or_assignee)
rules.add_perm("tasks.move_task", is_card_owner_or_assignee)
