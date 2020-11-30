# Django
from django.urls import path

# Local
from . import views

app_name = "cards"

urlpatterns = [
    path("<int:card_id>/", views.card_detail, name="card_detail"),
    path("<int:card_id>/~edit/", views.edit_card, name="edit_card"),
    path("<int:card_id>/~delete/", views.delete_card, name="delete_card"),
    path("<int:project_id>/~create/", views.create_card, name="create_card"),
    path("<int:column_id>/~move/", views.move_cards, name="move_cards"),
    path(
        "<int:column_id>/<int:swimlane_id>/~move/",
        views.move_cards,
        name="move_cards_in_swimlane",
    ),
    path(
        "<int:project_id>/<int:column_id>/~create/",
        views.create_card,
        name="create_card_for_column",
    ),
]
