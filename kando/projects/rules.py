# Third Party Libraries
import rules


@rules.predicate
def is_owner(user, project):
    return user == project.owner


@rules.predicate
def is_member(user, project):
    return user.is_authenticated and user.is_member(project)


@rules.predicate
def is_manager(user, project):
    return user.is_authenticated and user.is_manager(project)


@rules.predicate
def is_admin(user, project):
    return user.is_authenticated and user.is_admin(project)


rules.add_perm("projects.change_project", is_owner | is_admin)
rules.add_perm("projects.delete_project", is_owner)
