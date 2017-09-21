from django import forms
from .models import Journal


class JournalForm(forms.Form):
    class Meta:
        model = Journal
        fields = ['title', 'text', 'image']

    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder':'First Day on the Job'}))
    text = forms.Textarea()
    image = forms.ImageField()