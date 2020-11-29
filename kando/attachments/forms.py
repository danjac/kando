# Django
from django import forms

# Local
from .models import Attachment


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ("file",)
