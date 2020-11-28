# Third Party Libraries
import rules

# Kando
from kando.projects.rules import (
    is_project_admin,
    is_project_manager,
    is_project_member,
    is_project_owner,
)


@rules.predicate
def is_card_project_member(user, card):
    return is_project_member(user, card.project)


@rules.predicate
def is_card_owner(user, card):
    return is_card_project_member(user, card) and user == card.owner


@rules.predicate
def is_card_project_manager(user, card):
    return is_project_manager(user, card.project)


@rules.predicate
def is_card_project_admin(user, card):
    return is_project_admin(user, card.project)


@rules.predicate
def is_card_project_owner(user, card):
    return is_project_owner(user, card.project)


@rules.predicate
def is_card_assignee(user, card):
    return user.is_authenticated and card.assignee == user


is_card_manager = (
    is_card_owner
    | is_card_project_manager
    | is_card_project_admin
    | is_card_project_owner
)

is_card_owner_or_assignee = is_card_owner | is_card_assignee


rules.add_perm(
    "cards.create_card", is_project_member | is_project_owner,
)

rules.add_perm(
    "cards.view_card", is_card_project_member | is_card_project_owner | is_card_assignee
)
rules.add_perm("cards.change_card", is_card_manager)
rules.add_perm("cards.move_card", is_card_manager | is_card_assignee)
rules.add_perm("cards.delete_card", is_card_manager)
