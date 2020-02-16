from django.shortcuts import render
from .forms import RegisterForm,LoginForm, ForgotForm,ResetForm
from .UsersManager import UsersManager
from .ErrorCodes import ErrorCodes
from colorama import Fore, Back, Style,init
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse

init()
def printf(text,color):
     print(color + text)
     print(Style.RESET_ALL)
# Create your views here.


def APIGetLoginInfo(request):
     if 'user_id' in request.COOKIES:
        user_id = request.COOKIES['user_id']
        session_id = request.COOKIES['session_id']
        userAgent = request.META['HTTP_USER_AGENT']
        if UsersManager.checkSession(user_id,session_id,userAgent) :
            userQuery = UsersManager.getUserFromId(user_id)
            return JsonResponse({'login':1,
                                       'firstName':userQuery.firstName,
                                       'familyName':userQuery.familyName,
                                       'email':userQuery.email,
                                       'number':userQuery.number,
                                       'privLevel':userQuery.privLevel})
     return JsonResponse({'login':0})


def APIRegister(request):
    if request.method == "POST":
        myform = RegisterForm(request.POST)
        if myform.is_valid():
            printf("Registration Request..",Fore.GREEN)
            myform.toLower()
            myform_cleaned = myform.cleaned_data
            newUser = UsersManager.getModelFromRegisterForm(myform_cleaned)
            result = UsersManager.validateInputFrom(newUser,myform_cleaned['pass1'],myform_cleaned['pass2'])
            if result == ErrorCodes.REGISTER_INPUTS.NONE:
                UsersManager.addNewUser(newUser)
                printf("Registration Completed",Fore.GREEN)
            elif result == ErrorCodes.REGISTER_INPUTS.PASSMISSMATCH:
                printf("data not valid : INVALID_INPUTS_PASSMISSMATCH",Fore.RED)
            elif result == ErrorCodes.REGISTER_INPUTS.EMAILEXISTS:
                printf("data not valid : INVALID_INPUTS_EMAILEXISTS",Fore.RED)
            elif result == ErrorCodes.REGISTER_INPUTS.USEREXISTS:
                printf("data not valid : INVALID_INPUTS_USEREXISTS",Fore.RED)
            else:
                printf("This should not happen!!!",Fore.RED)
            return JsonResponse({'Status':result})
        else:
            return HttpResponse(status=400)
    else:# other than POST request returns 404 error
        return HttpResponse(status=404)

def APILogin(request):
    if request.method == "POST":
        myform = LoginForm(request.POST)

        if myform.is_valid():
            myform.toLower()
            myform_cleaned = myform.cleaned_data
            userQuery = UsersManager.getModelFromLoginForm(myform_cleaned['email'])
            result = UsersManager.checkUser(userQuery,myform_cleaned['password'])
            if result == ErrorCodes.LOGIN_INPUTS.NONE:
                printf("Successful Login.",Fore.GREEN)
                newToken = UsersManager.saveSession(userQuery,request.META['HTTP_USER_AGENT'])
                response = JsonResponse({'Status':0})
                response.set_cookie('session_id',newToken)
                response.set_cookie('user_id',userQuery.first().id)
                return response
            else:
                if result == ErrorCodes.LOGIN_INPUTS.EMAIL_NOT_FOUND:
                    printf("Email does not exist!",Fore.RED)
                elif result == ErrorCodes.LOGIN_INPUTS.PASS_MISMATCH:
                    printf("Wrong password!",Fore.RED)
                return JsonResponse({'Status':result})
        else:
            return HttpResponse(status=400)
    else:# other than POST request returns 404 error
        return HttpResponse(status=404)


def APILogout(request):
    response = JsonResponse({'Status':0})
    user_id = request.COOKIES['user_id']
    session_id = request.COOKIES['session_id']
    UsersManager.deleteSession(user_id,session_id)
    response.delete_cookie('session_id','')
    response.delete_cookie('user_id','')
    return response

def APIForgotPassword(request):
    if request.method == "POST":
        myform = ForgotForm(request.POST)
        if myform.is_valid():
            myform.toLower()
            userQuery = UsersManager.getModelFromLoginForm(myform.cleaned_data['email'])
            result = UsersManager.checkEmail(userQuery)
            if result == ErrorCodes.FORGOT_INPUTS.NONE:
                Token = UsersManager.savePassResetToken(userQuery)
                printf("Password reset token = " + Token,Fore.GREEN)
                #TODO: send token to the email
            elif result == ErrorCodes.FORGOT_INPUTS.EMAIL_NOT_FOUND :
                error = 1
                printf("Email does not exist.",Fore.RED)
            return JsonResponse({'Status':result})

        else:
            return HttpResponse(status=400)
    else:# other than POST request returns 404 error
        return HttpResponse(status=404)


def APIResetPassword(request):
    if request.method == "POST":
        myform = ResetForm(request.POST)
        if myform.is_valid():
            myform_cleaned = myform.cleaned_data
            fromToken = myform_cleaned['token']
            fromPass = myform_cleaned['password']
            result = UsersManager.isValidResetToken(fromToken)
            if  result == ErrorCodes.FORGOT_INPUTS.NONE:
                UsersManager.changePassword(fromToken,fromPass)
                UsersManager.deleteToken(fromToken)
            elif result == ErrorCodes.FORGOT_INPUTS.INVALID_TOKEN:
                printf("Email does not exists.",Fore.RED)
            return JsonResponse({'Status':result})
        else:
            return HttpResponse(status=400)
    else:# other than POST request returns 404 error
        return HttpResponse(status=404)

#TODO: Do logs for all operations specially the ones with 400 error 'couse it's probably hacking attempts