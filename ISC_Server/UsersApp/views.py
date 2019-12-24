from django.shortcuts import render
from .forms import RegisterForm,LoginForm, ForgotForm,ResetForm
from .UsersManager import UsersManager
from .ErrorCodes import ErrorCodes
from colorama import Fore, Back, Style,init
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

init()
def printf(text,color):
     print(color + text)
     print(Style.RESET_ALL)
# Create your views here.

def Home(request):
    
    if 'user_id' in request.COOKIES:
        user_id  = request.COOKIES['user_id']
        session_id = request.COOKIES['session_id']
        userAgent = request.META['HTTP_USER_AGENT']
        if UsersManager.checkSession(user_id,session_id,userAgent) :
            userQuery = UsersManager.getUserFromId(user_id)
            return render(request,"UsersApp/index.html",{'login':1,'userName':userQuery.firstName})
    return render(request,"UsersApp/index.html",{'login':0})


def Register(request):
    if request.method == "POST":
        
        myform = RegisterForm(request.POST)
        if myform.is_valid():
            printf("Gotcha ...",Fore.GREEN)
            newUser = UsersManager.getModelFromRegisterForm(myform.cleaned_data)
            result = UsersManager.validateInputFrom(newUser,myform.cleaned_data['pass1'],myform.cleaned_data['pass2'])
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
            userQuery = UsersManager.getModelFromLoginForm(myform.cleaned_data['email'])
            result = UsersManager.checkUser(userQuery,myform.cleaned_data['password'])
            if result ==  ErrorCodes.LOGIN_INPUTS.NONE:
                
                newToken = UsersManager.saveSession(userQuery,request.META['HTTP_USER_AGENT'])
                printf("Login: all Good",Fore.GREEN)
                response = redirect("home-page")
                response.set_cookie('session_id',newToken)
                response.set_cookie('user_id',userQuery.first().id)
                return response
            else:
                error = 0
                if result ==  ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND:
                    printf("Email does not exist",Fore.RED)
                    error = 1
                elif result ==  ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND:
                    printf("Multiple Emails in database !!",Fore.RED)
                    error = 3
                elif result ==  ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH:
                    printf("Wrong password",Fore.RED)
                    error = 2
                return render(request,"UsersApp/login.html",{'error':error})

    return render(request,"UsersApp/login.html")


def Logout(request):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.delete_cookie('session_id','')
    response.delete_cookie('user_id','')
    return response

def forgotPassword(request):
    if request.method == "POST":
        myform = ForgotForm(request.POST)
        if myform.is_valid():
            userQuery = UsersManager.getModelFromLoginForm(myform.cleaned_data['email'])
            result = UsersManager.checkEmail(userQuery)
            if result == ErrorCodes.FORGOT_INPUTS.NONE:
                Token = UsersManager.savePassResetToken(userQuery)
                printf("Password reset token = " + Token,Fore.GREEN)
                #TODO: send token to the email
                return redirect("reset-pass-page")
            elif result == ErrorCodes.FORGOT_INPUTS.EMAIL_NOT_FOUND :
                 error = 1
                 printf("Email does not exist",Fore.RED)
                 return render(request,"UsersApp/forgotPass.html",{'error':error})

    return render(request,"UsersApp/forgotPass.html")


def ResetPassword(request):
    if request.method == "POST":
        myform = ResetForm(request.POST)
        if myform.is_valid():
            fromToken = myform.cleaned_data['token']
            fromPass = myform.cleaned_data['password']
            result  = UsersManager.isValidResetToken(fromToken)
            if  result == ErrorCodes.FORGOT_INPUTS.NONE:
                UsersManager.changePassword(fromToken,fromPass)
                UsersManager.deleteToken(fromToken)
                return redirect("login-page")
            elif result == ErrorCodes.FORGOT_INPUTS.INVALID_TOKEN:
                error = 1
                printf("Email does not exists",Fore.RED)
                return render(request,"UsersApp/resetPass.html",{'error':error})

                

    return render(request,"UsersApp/resetPass.html")

