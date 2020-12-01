# Django
from django.urls import path

# Local
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.projects_overview, name="projects_overview"),
    path("<int:project_id>/board/", views.project_board, name="project_board"),
    path("<int:project_id>/members/", views.project_members, name="project_members"),
    path(
        "<int:member_id>/~/change-role/",
        views.change_member_role,
        name="change_member_role",
    ),
    path("<int:member_id>/~/remove/", views.remove_member, name="remove_member",),
    path(
        "<int:project_id>/member/<slug:username>/",
        views.project_member_detail,
        name="member_detail",
    ),
    path("<int:project_id>/~edit/", views.edit_project, name="edit_project"),
    path("<int:project_id>/~delete/", views.delete_project, name="delete_project"),
    path(
        "<int:project_id>/~duplicate/",
        views.duplicate_project,
        name="duplicate_project",
    ),
    path("~create/", views.create_project, name="create_project"),
]
