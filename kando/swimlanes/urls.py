# Django
from django.urls import path

# Local
from . import views

app_name = "swimlanes"

urlpatterns = [
    path("<int:project_id>/~create/", views.create_swimlane, name="create_swimlane"),
    # path("<int:project_id>/~move/", views.move_swimlanes, name="move_swimlanes"),
    # path("<int:swimlane_id>/", views.swimlane_detail, name="swimlane_detail"),
    # path("<int:swimlane_id>/~edit/", views.edit_swimlane, name="edit_swimlane"),
    # path("<int:swimlane_id>/~delete/", views.delete_swimlane, name="delete_swimlane"),
]
