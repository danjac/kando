# Third Party Libraries
import rules


@rules.predicate
def is_project_owner(user, project):
    return user == project.owner


@rules.predicate
def is_project_member(user, project):
    return user.is_authenticated and user.is_member(project)


@rules.predicate
def is_project_manager(user, project):
    return user.is_authenticated and user.is_manager(project)


@rules.predicate
def is_project_admin(user, project):
    return user.is_authenticated and user.is_admin(project)


is_project_owner_or_admin = is_project_owner | is_project_admin

rules.add_perm("projects.view_project", is_project_owner | is_project_member)
rules.add_perm("projects.change_project", is_project_owner_or_admin)
rules.add_perm("projects.delete_project", is_project_owner)
