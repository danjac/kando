# Django
from django import forms

# Local
from .models import Swimlane


class SwimlaneForm(forms.ModelForm):
    class Meta:
        model = Swimlane
        fields = ("name",)
