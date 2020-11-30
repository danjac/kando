# Django
from django import forms

# Local
from .models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            "name",
            "assignee",
            "description",
            "complexity",
            "priority",
            "hours_estimated",
            "column",
            "swimlane",
        )

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)
        project = project or self.instance.project
        if project is None:
            raise ValueError(
                "Project must be provided as argument or with card instance"
            )
        self.project = project

        self.fields["column"].queryset = self.project.column_set.order_by("position")

        swimlanes = self.project.swimlane_set.order_by("position")
        if swimlanes.count() == 0:
            del self.fields["swimlane"]
        else:
            self.fields["swimlane"].queryset = swimlanes

        users_qs = self.project.members.order_by("name", "username")

        if users_qs.count() == 0:
            del self.fields["assignee"]
        else:
            self.fields["assignee"].queryset = users_qs
