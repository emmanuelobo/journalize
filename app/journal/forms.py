from django.forms import forms
from .models import Journal


class JournalForm(forms.Form):
    class Meta:
        model = Journal
        fields = ['title', 'text',]