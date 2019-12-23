from django.shortcuts import render
from .models import SessionsDB, UsersDB
from ISC_Server.UsersApp.UsersManager import UsersManager
# Create your views here.
from django.core.mail import send_mail





def Home(request):
    
    if 'user_id' in request.COOKIES:
        user_id  = request.COOKIES['user_id']
        session_id = request.COOKIES['session_id']
        userAgent = request.META['HTTP_USER_AGENT']
        if UsersManager.checkSession(user_id,session_id,userAgent) :
            userQuery = UsersManager.getUserFromId(user_id)
            return render(request,"MainApp/index.html",{'login':1,'username':userQuery.firstName})

    return render(request,"MainApp/index.html",{'login':0})