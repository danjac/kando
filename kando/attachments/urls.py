# Django
from django.urls import path

# Local
from . import views

app_name = "attachments"

urlpatterns = [
    path("<int:card_id>/~/create/", views.create_attachment, name="create_attachment"),
    path(
        "<int:attachment_id>/~/delete/",
        views.delete_attachment,
        name="delete_attachment",
    ),
]
