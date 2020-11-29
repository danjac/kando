# Third Party Libraries
import rules

# Kando
from kando.projects.rules import is_project_owner_or_admin


@rules.predicate
def is_column_project_owner_or_admin(user, column):
    return is_project_owner_or_admin(user, column.project)


rules.add_perm("columns.create_column", is_project_owner_or_admin)
rules.add_perm("columns.move_columns", is_project_owner_or_admin)
rules.add_perm("columns.change_column", is_column_project_owner_or_admin)
rules.add_perm("columns.delete_column", is_column_project_owner_or_admin)
