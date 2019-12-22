from django.shortcuts import render
from .forms import RegisterForm,LoginForm
from .RegisterManager import UsersManager
from .ErrorCodes import ErrorCodes
from colorama import Fore, Back, Style,init
from django.shortcuts import redirect

init()
def printf(text,color):
     print(color + text)
     print(Style.RESET_ALL)
# Create your views here.
def Register(request):
    if request.method == "POST":
        myform = RegisterForm(request.POST)
        if myform.is_valid():
            newUser = UsersManager.getModelFromRegisterForm(myform.cleaned_data)
            result = UsersManager.validateInputFrom(newUser,myform.cleaned_data)
            if result == ErrorCodes.REGISTER_INPUTS.NONE:
                UsersManager.addNewUser(newUser)
                printf("All Good",Fore.GREEN)
                return redirect("login-page")
            else:
                error = 0
                if result == ErrorCodes.REGISTER_INPUTS.PASSMISSMATCH:
                    printf("data not valid : INVALID_INPUTS_PASSMISSMATCH",Fore.RED)
                    error = 3
                elif result == ErrorCodes.REGISTER_INPUTS.EMAILEXISTS:
                    error = 2
                    printf("data not valid : INVALID_INPUTS_EMAILEXISTS",Fore.RED)
                elif result == ErrorCodes.REGISTER_INPUTS.USEREXISTS:
                    error = 1
                    printf("data not valid : INVALID_INPUTS_USEREXISTS",Fore.RED)
                else:
                    printf("This should not happen!!!",Fore.RED)
                return render(request,"UsersApp/register.html",{'error':error})
    return render(request,"UsersApp/register.html")

def Login(request):
    if request.method == "POST":
        myform = LoginForm(request.POST)
        
        if myform.is_valid():
            userQuery = UsersManager.getModelFromLoginForm(myform.cleaned_data)
            result = UsersManager.checkUser(userQuery,myform.cleaned_data)
            if result ==  ErrorCodes.LOGIN_INPUTS.NONE:
                UsersManager.saveSession(userQuery)
                printf("Login: all Good",Fore.GREEN)
                return redirect("home-page")
            else:
                error = 0
                if result ==  ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND:
                    printf("Email does not exists",Fore.RED)
                    error = 1
                elif result ==  ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND:
                    printf("Multiple Emails in database !!",Fore.RED)
                    error = 3
                elif result ==  ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH:
                    printf("Wrong password",Fore.RED)
                    error = 2
                return render(request,"UsersApp/login.html",{'error':error})

    return render(request,"UsersApp/login.html")




