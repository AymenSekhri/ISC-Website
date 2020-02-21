from django import forms
from django.core.validators import RegexValidator

class RegisterForm(forms.Form):
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    nums = RegexValidator(r'^[0-9]*$', 'Only alphanumeric characters are allowed.')

    firstName = forms.CharField(max_length=30, min_length = 3, validators=[alpha])
    familyName = forms.CharField(max_length=30, min_length = 3, validators=[alpha])
    email = forms.EmailField()
    pass1 = forms.CharField(min_length = 8)
    pass2 = forms.CharField(min_length = 8)
    number = forms.CharField(max_length=20,validators=[nums])
    year = forms.CharField(max_length=4,validators=[nums])

    def toLower(self):
        self.cleaned_data["firstName"] = self.cleaned_data["firstName"].lower()
        self.cleaned_data["familyName"] = self.cleaned_data["familyName"].lower()
        self.cleaned_data["email"] = self.cleaned_data["email"].lower()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def toLower(self):
        self.cleaned_data["email"] = self.cleaned_data["email"].lower()

class ForgotForm(forms.Form):
    email = forms.EmailField()

    def toLower(self):
        self.cleaned_data["email"] = self.cleaned_data["email"].lower()

class ResetForm(forms.Form):
    password = forms.CharField()
    token = forms.CharField()

class CreateEventForm(forms.Form):
    
    eventName = forms.CharField()
    description = forms.CharField()
    deadline_date = forms.CharField()
    event_date = forms.CharField()
    maxNumberOfEnrolment = forms.IntegerField()
    enrollmentData = forms.CharField()
    
class EnrollEventForm(forms.Form):
    response = forms.CharField()

class ManageEventsForm(forms.Form):
    cmd = forms.CharField()

class DecisionForm(forms.Form):
    nums = RegexValidator(r'^[0-2]*$', 'Only alphanumeric characters are allowed.')
    userID = forms.CharField()
    decision = forms.IntegerField(validators=[nums])

class PostponeEventsForm(forms.Form):
    cmd = forms.CharField()
    newDate = forms.CharField()

class PostsForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
    tags = forms.CharField()

class AddToTeamFrom(forms.Form):
    userID = forms.IntegerField()
    title = forms.CharField()
    bio = forms.CharField()
    contacts = forms.CharField()


class EditMemberFrom(forms.Form):
    title = forms.CharField()
    bio = forms.CharField()
    contacts = forms.CharField()

class EditUserFrom(forms.Form):
    firstName = forms.CharField()
    familyName = forms.CharField()
    email = forms.CharField()
    number = forms.CharField()

class UpgradeUserForm(forms.Form):
    newLevel = forms.IntegerField()

