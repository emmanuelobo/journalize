from django.contrib.auth.models import User
from django.forms import ModelForm


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
