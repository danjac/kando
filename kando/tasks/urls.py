# Django
from django.urls import path

# Local
from . import views

app_name = "tasks"

urlpatterns = [
    path("<int:card_id>/~/create/", views.create_task, name="create_task"),
]
