# Django
from django.urls import path

# Local
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.projects_overview, name="project_overview"),
    path("~create/", views.create_project, name="create_project"),
]
