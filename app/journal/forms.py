from django import forms
from django.forms import ModelForm

from .models import Journal


class JournalForm(ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control', 'style': "width: 100%;height: 120px;font-size: 70px;font-family: 'Tahoma', sans-serif;"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'What\'s on your mind today?', 'style': 'width:100%; height:150px;margin-bottom: 30px;font-size:40px;', 'class': 'form-control'}))
    image = forms.ImageField(required=False)
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'hidden'}))

    class Meta:
        model = Journal
        fields = ['title', 'text', 'image']