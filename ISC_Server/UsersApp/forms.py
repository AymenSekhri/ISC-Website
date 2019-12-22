from django import forms

class RegisterForm(forms.Form):
    firstName = forms.CharField(max_length=30)
    familyName = forms.CharField(max_length=30)
    email = forms.EmailField()
    pass1 = forms.CharField()
    pass2 = forms.CharField()
    number = forms.CharField(max_length=20)
    year = forms.CharField(max_length=4)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
