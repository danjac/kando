# Third Party Libraries
import rules

# Kando
from kando.cards.rules import is_card_owner_or_assignee


@rules.predicate
def is_task_card_owner_or_assignee(user, task):
    return user.is_authenticated and is_card_owner_or_assignee(user, task.card)


rules.add_perm("tasks.create_task", is_card_owner_or_assignee)
rules.add_perm("tasks.move_tasks", is_card_owner_or_assignee)
rules.add_perm("tasks.change_task", is_task_card_owner_or_assignee)
rules.add_perm("tasks.delete_task", is_task_card_owner_or_assignee)
