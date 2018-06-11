from django.contrib.auth.models import User
from django.forms import ModelForm, forms
from django import forms


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={"placeholder": "jbsmooth", "class": "form-control"}
        ),
        required=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "shhhhh..", "class": "form-control"}
        ),
    )


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control"}), required=False
    )
    profile_pic = forms.ImageField(required=False)
