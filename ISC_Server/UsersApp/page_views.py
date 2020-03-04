from django.shortcuts import render
from .API_Functionality import *

def Home(request):
    if request.method == "GET":
        #check if user is logged
        if checkPrivLevel(request, UserPermission.VALIDUSER):
            return render(request,"UsersApp/index.html")
        else:#in case if user not logged go to login
            return render(request,"UsersApp/login.html")

def Login(request):
    return render(request,"UsersApp/login.html")

def Register(request):
    return render(request,"UsersApp/register.html")

def ResetPassword(request):
    return render(request,"UsersApp/resetpass.html")

def ForgotPassword(request):
    return render(request,"UsersApp/forgotPass.html")
