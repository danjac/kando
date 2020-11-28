# Django
from django import forms

# Local
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("description",)
