from django import forms

class RegisterForm(forms.Form):
    firstName = forms.CharField(max_length=30)
    familyName = forms.CharField(max_length=30)
    email = forms.EmailField()
    pass1 = forms.CharField(max_length=256)
    pass2 = forms.CharField(max_length=256)
    number = forms.CharField(max_length=20)
    year = forms.CharField(max_length=4)
