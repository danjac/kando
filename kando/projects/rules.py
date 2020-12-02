# Third Party Libraries
import rules


@rules.predicate
def is_project_owner(user, project):
    return user == project.owner


@rules.predicate
def is_project_member(user, project):
    return user.is_authenticated and user.is_project_member(project)


@rules.predicate
def is_project_manager(user, project):
    return user.is_authenticated and user.is_project_manager(project)


@rules.predicate
def is_project_admin(user, project):
    return user.is_authenticated and user.is_project_admin(project)


is_project_owner_or_member = is_project_owner | is_project_member
is_project_owner_or_admin = is_project_owner | is_project_admin


@rules.predicate
def is_member_project_owner_or_admin(user, member):
    return is_project_owner_or_admin(user, member.project)


@rules.predicate
def is_member_self(user, member):
    return member.user == user


rules.add_perm("projects.view_project", is_project_owner_or_member)
rules.add_perm("projects.change_project", is_project_owner_or_admin)
rules.add_perm("projects.delete_project", is_project_owner)

rules.add_perm("projects.add_members", is_project_owner_or_admin)

rules.add_perm(
    "projects.remove_member", is_member_project_owner_or_admin & ~is_member_self
)
rules.add_perm(
    "projects.change_member_role", is_member_project_owner_or_admin & ~is_member_self
)
