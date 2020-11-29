# Django
from django import forms

# Local
from .models import Column


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ("name",)
