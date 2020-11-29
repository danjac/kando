# Django
from django.urls import path

# Local
from . import views

app_name = "tasks"

urlpatterns = [
    path("<int:card_id>/~/create/", views.create_task, name="create_task"),
    path("<int:card_id>/~/move/", views.move_tasks, name="move_tasks"),
    path("<int:task_id>/~/edit/", views.edit_task, name="edit_task"),
    path("<int:task_id>/~/delete/", views.delete_task, name="delete_task"),
    path(
        "<int:task_id>/~/toggle-complete/",
        views.toggle_complete,
        name="toggle_complete",
    ),
]
