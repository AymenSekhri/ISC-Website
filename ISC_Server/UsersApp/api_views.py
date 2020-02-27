from django.shortcuts import render
from django.http import HttpResponse
from .API_Functionality import *
from .UsersManager import *




#Authentication
def APIGetLoginInfo(request):
    if request.method == "GET":
        if checkPrivLevel(request, UserPermission.VALIDUSER):
            return getCurrentUserInfo(request)
    return HttpResponse(status=400)

def APIRegister(request):
    if request.method == "POST":
        return register(request)
    return HttpResponse(status=400)

def APILogin(request):
    if request.method == "POST":
        return login(request)
    return HttpResponse(status=400)

def APILogout(request):
    if checkPrivLevel(request, UserPermission.VALIDUSER):
        return logout(request)
    return HttpResponse(status=400)

def APIForgotPassword(request):
    if request.method == "POST":
        return forgotPassword(request)
    return HttpResponse(status=400)

def APIResetPassword(request):
    if request.method == "POST":
        return ResetPassword(request)
    return HttpResponse(status=400)

#Events
def APICreateEvent(request):
    if request.method == "POST":
        if checkPrivLevel(request,UserPermission.CreateEvent):
            return createEvent(request)
    return HttpResponse(status=400)

def APIEnrollEvent(request,id):#id = the id of the event
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.EnrollEvent):
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
        if checkPrivLevel(request,UserPermission.ManageEvent):
            return ManageEvent(id, request)
   return HttpResponse(status=400)

def APIListEnrollmentsOfEvent(request,id):
   if request.method == "GET":
        if checkPrivLevel(request,UserPermission.ViewEnrollments):
            return getEnrollmentList(id, request)
   return HttpResponse(status=400)

def APIMakeDecision(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.Decision):
            return makeEnrollmentDecision(id, request)
   return HttpResponse(status=400)

def APIPostponeEvent(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.PostponeEvent):
            return postponeEvent(id, request)
   return HttpResponse(status=400)

#News
def APICreateNewsPost(request):
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.CreateNews):
            return createPost(request,POST_TYPE.NEWS)
   return HttpResponse(status=400)

def APIGetNewsPostsList(request):
   if request.method == "GET":
        return getPostsList(POST_TYPE.NEWS)
   return HttpResponse(status=400)

def APIGetNewsPostDetails(request,id):
   if request.method == "GET":
        return getPostDetails(id,POST_TYPE.NEWS)
   return HttpResponse(status=400)

def APIEditNewsPost(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.EditNews):
            return editPost(id,POST_TYPE.NEWS, request)
   return HttpResponse(status=400)

def APIDeleteNewsPost(request,id):
   if request.method == "GET":
        if checkPrivLevel(request,UserPermission.DeleteNews):
            return deletePost(id, POST_TYPE.NEWS, request)
   return HttpResponse(status=400)

#Projects
def APICreateProjectPost(request):
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.CreateProject):
            return createPost(request,POST_TYPE.PROJECT)
   return HttpResponse(status=400)

def APIGetProjectPostsList(request):
   if request.method == "GET":
        return getPostsList(POST_TYPE.PROJECT)
   return HttpResponse(status=400)

def APIGetProjectPostDetails(request,id):
   if request.method == "GET":
        return getPostDetails(id,POST_TYPE.PROJECT)
   return HttpResponse(status=400)

def APIEditProjectPost(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.EditProject):
            return editPost(id,POST_TYPE.PROJECT, request)
   return HttpResponse(status=400)

def APIDeleteProjectPost(request,id):
   if request.method == "GET":
        if checkPrivLevel(request,UserPermission.DeleteProject):
            return deletePost(id, POST_TYPE.PROJECT,request)
   return HttpResponse(status=400)

# Team
def APIAddToTheTeam(request):
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.TeamAdd):
            return addMember(request)
   return HttpResponse(status=400)

def APIGetTeamList(request):
   if request.method == "GET":
        return getMembers()
   return HttpResponse(status=400)

def APIEditTeamMember(request,id):
   if request.method == "POST":
        if checkPrivLevel(request,UserPermission.TeamEdit):
            return editMember(id, request)
   return HttpResponse(status=400)

def APIDeleteTeamMember(request,id):
   if request.method == "GET":
        if checkPrivLevel(request,UserPermission.TeamDelete):
            return deleteMember(id, request)
   return HttpResponse(status=400)

#users
def APIGetUsersList(request):
   if request.method == "GET":
       if checkPrivLevel(request,UserPermission.UsersList):
            return getUsersList(request)
   return HttpResponse(status=400)

def APIGetUserDetails(request, id):
   if request.method == "GET":
       if checkPrivLevel(request,UserPermission.ViewUserInfo):
            return getUserDetails(id)
   return HttpResponse(status=400)

def APIEditUserProfile(request, id):
   if request.method == "POST":
       if checkPrivLevel(request,UserPermission.EditUserInfo):
            return editUserProfile(id, request)
   return HttpResponse(status=400)

def APIDeleteUser(request, id):
   if request.method == "GET":
       if checkPrivLevel(request,UserPermission.DeleteUser):
            return deleteUser(id)
   return HttpResponse(status=400)

def APIUpgradeUser(request, id):
   if request.method == "POST":
       if checkPrivLevel(request,UserPermission.ChangeUserPermission):
            return upgradeUser(id, request)
   return HttpResponse(status=400)

