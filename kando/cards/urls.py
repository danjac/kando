# Django
from django.urls import path

# Local
from . import views

app_name = "cards"

urlpatterns = [
    path("<int:project_id>/~create/", views.create_card, name="create_card"),
    path(
        "<int:project_id>/<int:column_id>/~create/",
        views.create_card,
        name="create_card_for_column",
    ),
]
