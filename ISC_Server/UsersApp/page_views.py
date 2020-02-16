from django.shortcuts import render

def Home(request):
    return render(request,"UsersApp/index.html")

def Login(request):
    return render(request,"UsersApp/login.html")

def Register(request):
    return render(request,"UsersApp/register.html")

def ResetPassword(request):
    return render(request,"UsersApp/resetpass.html")

def ForgotPassword(request):
    return render(request,"UsersApp/forgotPass.html")
