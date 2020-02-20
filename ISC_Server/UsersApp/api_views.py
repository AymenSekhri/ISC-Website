from django.shortcuts import render
from django.http import HttpResponse
from .API_Functionality import *


# Create your views here.

def APIGetLoginInfo(request):
    if request.method == "GET":
        return getCurrentUserInfo(request)
    else:
        return HttpResponse(status=400)

def APIRegister(request):
    if request.method == "POST":
        return register(request)
    else:
        return HttpResponse(status=400)

def APILogin(request):
    if request.method == "POST":
        return login(request)
    else:
        return HttpResponse(status=400)

def APILogout(request):
    return logout(request)

def APIForgotPassword(request):
    if request.method == "POST":
        return forgotPassword(request)
    else:
        return HttpResponse(status=400)

def APIResetPassword(request):
    if request.method == "POST":
        return ResetPassword(request)
    else:
        return HttpResponse(status=400)

def APICreateEvent(request):
    if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return createEvent(request)
    return HttpResponse(status=400)

def APIEnrollEvent(request,id):#id = the id of the event
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return enrollEvent(id, request)
   return HttpResponse(status=400)

def APIListEvents(request):
    if request.method == "GET":
        return getEventsList()
    return HttpResponse(status=400)

def APIEventInfo(request,id):
    if request.method == "GET":
        return getEventInfo(id)
    return HttpResponse(status=400)

def APIManageEvent(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return ManageEvent(id, request)
   return HttpResponse(status=400)

def APIListEnrollmentsOfEvent(request,id):
   if request.method == "GET":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return getEnrollmentList(id, request)
   return HttpResponse(status=400)

def APIMakeDecision(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return makeEnrollmentDecision(id, request)
   return HttpResponse(status=400)

def APIPostponeEvent(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,PRIVILEGE_LEVEL_0):
            return postponeEvent(id, request)
   return HttpResponse(status=400)
