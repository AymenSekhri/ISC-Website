from django.shortcuts import render
from .models import SessionsDB, UsersDB
from ISC_Server.UsersApp.UsersManager import UsersManager
# Create your views here.
from django.core.mail import send_mail





def Home(request):
    
    return render(request,"MainApp/index.html",{'login':0})