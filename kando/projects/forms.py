# Django
from django import forms
from django.utils.translation import gettext_lazy as _

# Local
from .models import Project, ProjectMember


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "name",
            "description",
        )
        labels = {"name": _("Project Name")}


class ProjectCreationForm(ProjectForm):
    def save(self, owner):
        return Project.objects.create_project(owner=owner, **self.cleaned_data)


class ProjectMemberRoleForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ("role",)
        widgets = {"role": forms.RadioSelect}
