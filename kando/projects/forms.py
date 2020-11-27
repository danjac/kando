# Django
from django import forms

# Local
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "is_private", "task_limit")


class ProjectCreationForm(ProjectForm):
    def save(self, owner):
        return Project.objects.create_project(owner=owner, **self.cleaned_data)
