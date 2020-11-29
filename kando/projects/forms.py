# Django
from django import forms
from django.utils.translation import gettext_lazy as _

# Local
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "task_limit")
        labels = {"name": _("Project Name")}
        help_texts = {
            "task_limit": _("Maximum number of cards per column"),
        }


class ProjectCreationForm(ProjectForm):
    def save(self, owner):
        return Project.objects.create_project(owner=owner, **self.cleaned_data)
