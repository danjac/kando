# Django
from django import forms
from django.utils.translation import gettext as _

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

        users_qs = self.project.members.order_by("name", "username")

        if users_qs.count() == 0:
            del self.fields["assignee"]
        else:
            self.fields["assignee"].queryset = users_qs

    def clean_column(self):
        column = self.cleaned_data["column"]
        card_count = self.project.card_set.filter(column=column).count()
        if self.project.task_limit and card_count >= self.project.task_limit:
            raise forms.ValidationError(
                _("You have exceeded the card limit of %(limit)s for this column"),
                params={"limit": self.project.task_limit},
            )
        return column
