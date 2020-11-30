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
        "<int:project_id>/member/<slug:username>/",
        views.project_member_detail,
        name="project_member_detail",
    ),
    path("<int:project_id>/~edit/", views.edit_project, name="edit_project"),
    path("<int:project_id>/~delete/", views.delete_project, name="delete_project"),
    path("~create/", views.create_project, name="create_project"),
]
