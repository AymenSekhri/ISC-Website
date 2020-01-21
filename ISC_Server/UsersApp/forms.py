from django import forms
from django.core.validators import RegexValidator

class RegisterForm(forms.Form):
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    firstName = forms.CharField(max_length=30, min_length = 3, validators=[alpha])
    familyName = forms.CharField(max_length=30, min_length = 3, validators=[alpha])
    email = forms.EmailField()
    pass1 = forms.CharField(min_length = 8)
    pass2 = forms.CharField(min_length = 8)
    number = forms.CharField(max_length=20)
    year = forms.CharField(max_length=4)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class ForgotForm(forms.Form):
    email = forms.EmailField()

class ResetForm(forms.Form):
    password = forms.CharField()
    token = forms.CharField()
