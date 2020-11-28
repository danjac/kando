# Django
from django.urls import path

# Local
from . import views

app_name = "invites"

urlpatterns = [
    path("<int:project_id>/~send/", views.send_invites, name="send_invites"),
    path("<str:invite_id>/~accept/", views.accept_invite, name="accept_invite"),
]
