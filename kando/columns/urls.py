# Django
from django.urls import path

# Local
from . import views

app_name = "columns"

urlpatterns = [
    path("<int:project_id>/~create/", views.create_column, name="create_column"),
    path("<int:project_id>/~move/", views.move_columns, name="move_columns"),
    path("<int:column_id>/~edit/", views.edit_column, name="edit_column"),
    path("<int:column_id>/~delete/", views.delete_column, name="delete_column"),
]
