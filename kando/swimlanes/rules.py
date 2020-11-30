# Third Party Libraries
import rules

# Kando
from kando.projects.rules import is_project_owner_or_admin, is_project_owner_or_member


@rules.predicate
def is_swimlane_project_owner_or_admin(user, swimlane):
    return is_project_owner_or_admin(user, swimlane.project)


@rules.predicate
def is_swimlane_project_owner_or_member(user, swimlane):
    return is_project_owner_or_member(user, swimlane.project)


rules.add_perm("swimlanes.create_swimlane", is_project_owner_or_admin)
rules.add_perm("swimlanes.move_swimlanes", is_project_owner_or_admin)
rules.add_perm("swimlanes.view_swimlane", is_swimlane_project_owner_or_member)
rules.add_perm("swimlanes.change_swimlane", is_swimlane_project_owner_or_admin)
rules.add_perm("swimlanes.delete_swimlane", is_swimlane_project_owner_or_admin)
