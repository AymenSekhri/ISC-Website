from django.shortcuts import render
from .models import UsersDB
from .forms import RegisterForm

# Create your views here.
def Register(request):
    if request.method == "POST":
        myform = RegisterForm(request.POST)
        if myform.is_valid():
            cleaned_form = myform.cleaned_data
            newUser = UsersDB(firstName=cleaned_form['firstName'],
                              familyName=cleaned_form['familyName'],
                              email=cleaned_form['email'],
                              password=cleaned_form['pass1'],## TODO: DUDE !!!! CHANGE THIS REAL SOON
                              salt = "123",
                              privLevel = 0,
                              number = cleaned_form['number'],
                              year = cleaned_form['year'])

            is_valid,error = newUser.validateInputs()
            if is_valid:
                newUser.save()
                print("all good")
            else:
                print("data not valid")
            #newUser.save()
    return render(request,"UsersApp/register.html")

def Login(request):
    return render(request,"UsersApp/login.html")